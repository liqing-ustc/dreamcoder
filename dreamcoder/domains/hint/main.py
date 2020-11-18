import random
from collections import defaultdict
import json
import math
import os
import datetime

from dreamcoder.dreamcoder import explorationCompression
from dreamcoder.utilities import eprint, flatten, testTrainSplit
from dreamcoder.grammar import Grammar
from dreamcoder.task import Task
from dreamcoder.type import Context, arrow, tbool, tlist, tint, t0, UnificationFailure
from dreamcoder.domains.hint.hintPrimitives import McCarthyPrimitives
from dreamcoder.recognition import RecurrentFeatureExtractor
from dreamcoder.domains.hint.makeTasks import make_list_bootstrap_tasks

def list_features(examples):
    if any(isinstance(i, int) for (i,), _ in examples):
        # obtain features for number inputs as list of numbers
        examples = [(([i],), o) for (i,), o in examples]
    elif any(not isinstance(i, list) for (i,), _ in examples):
        # can't handle non-lists
        return []
    elif any(isinstance(x, list) for (xs,), _ in examples for x in xs):
        # nested lists are hard to extract features for, so we'll
        # obtain features as if flattened
        examples = [(([x for xs in ys for x in xs],), o)
                    for (ys,), o in examples]

    # assume all tasks have the same number of examples
    # and all inputs are lists
    features = []
    ot = type(examples[0][1])

    def mean(l): return 0 if not l else sum(l) / len(l)
    imean = [mean(i) for (i,), o in examples]
    ivar = [sum((v - imean[idx])**2
                for v in examples[idx][0][0])
            for idx in range(len(examples))]

    # DISABLED length of each input and output
    # total difference between length of input and output
    # DISABLED normalized count of numbers in input but not in output
    # total normalized count of numbers in input but not in output
    # total difference between means of input and output
    # total difference between variances of input and output
    # output type (-1=bool, 0=int, 1=list)
    # DISABLED outputs if integers, else -1s
    # DISABLED outputs if bools (-1/1), else 0s
    if ot == list:  # lists of ints or bools
        omean = [mean(o) for (i,), o in examples]
        ovar = [sum((v - omean[idx])**2
                    for v in examples[idx][1])
                for idx in range(len(examples))]

        def cntr(
            l, o): return 0 if not l else len(
            set(l).difference(
                set(o))) / len(l)
        cnt_not_in_output = [cntr(i, o) for (i,), o in examples]

        #features += [len(i) for (i,), o in examples]
        #features += [len(o) for (i,), o in examples]
        features.append(sum(len(i) - len(o) for (i,), o in examples))
        #features += cnt_not_int_output
        features.append(sum(cnt_not_in_output))
        features.append(sum(om - im for im, om in zip(imean, omean)))
        features.append(sum(ov - iv for iv, ov in zip(ivar, ovar)))
        features.append(1)
        # features += [-1 for _ in examples]
        # features += [0 for _ in examples]
    elif ot == bool:
        outs = [o for (i,), o in examples]

        #features += [len(i) for (i,), o in examples]
        #features += [-1 for _ in examples]
        features.append(sum(len(i) for (i,), o in examples))
        #features += [0 for _ in examples]
        features.append(0)
        features.append(sum(imean))
        features.append(sum(ivar))
        features.append(-1)
        # features += [-1 for _ in examples]
        # features += [1 if o else -1 for o in outs]
    else:  # int
        def cntr(
            l, o): return 0 if not l else len(
            set(l).difference(
                set(o))) / len(l)
        cnt_not_in_output = [cntr(i, [o]) for (i,), o in examples]
        outs = [o for (i,), o in examples]

        #features += [len(i) for (i,), o in examples]
        #features += [1 for (i,), o in examples]
        features.append(sum(len(i) for (i,), o in examples))
        #features += cnt_not_int_output
        features.append(sum(cnt_not_in_output))
        features.append(sum(o - im for im, o in zip(imean, outs)))
        features.append(sum(ivar))
        features.append(0)
        # features += outs
        # features += [0 for _ in examples]

    return features

def list_options(parser):
    parser.add_argument("--maxTasks", type=int,
                        default=None,
                        help="truncate tasks to fit within this boundary")
    parser.add_argument("--extractor", type=str,
                        choices=["hand", "deep", "learned"],
                        default="learned")
    parser.add_argument("--split", metavar="TRAIN_RATIO",
                        type=float,
                        help="split test/train")
    parser.add_argument("-H", "--hidden", type=int,
                        default=64,
                        help="number of hidden units")
    parser.add_argument("--random-seed", type=int, default=49)

def isListFunction(tp):
    try:
        Context().unify(tp, arrow(tlist(tint), t0))
        return True
    except UnificationFailure:
        return False


def isIntFunction(tp):
    try:
        Context().unify(tp, arrow(tint, t0))
        return True
    except UnificationFailure:
        return False


class LearnedFeatureExtractor(RecurrentFeatureExtractor):
    H = 64
    
    special = None

    def tokenize(self, examples):
        def sanitize(l): return [z if z in self.lexicon else "?"
                                 for z_ in l
                                 for z in (z_ if isinstance(z_, list) else [z_])]

        tokenized = []
        for xs, y in examples:
            if isinstance(y, list):
                y = ["LIST_START"] + y + ["LIST_END"]
            else:
                y = [y]
            y = sanitize(y)
            if len(y) > self.maximumLength:
                return None

            serializedInputs = []
            for xi, x in enumerate(xs):
                if isinstance(x, list):
                    x = ["LIST_START"] + x + ["LIST_END"]
                else:
                    x = [x]
                x = sanitize(x)
                if len(x) > self.maximumLength:
                    return None
                serializedInputs.append(x)
            #     if '?' in x: break
            
            # if '?' in y or '?' in serializedInputs[-1]:
            #     continue

            tokenized.append((tuple(serializedInputs), y))

        return tokenized

    def __init__(self, tasks, testingTasks=[], cuda=False):
        self.lexicon = set(flatten((t.examples for t in tasks + testingTasks), abort=lambda x: isinstance(
            x, str))).union({"LIST_START", "LIST_END", "?"})
        # self.lexicon = list(range(20)) + ["LIST_START", "LIST_END", "?"]

        # Calculate the maximum length
        self.maximumLength = float('inf') # Believe it or not this is actually important to have here
        self.maximumLength = max(len(l)
                                 for t in tasks + testingTasks
                                 for xs, y in self.tokenize(t.examples)
                                 for l in [y] + [x for x in xs])

        self.recomputeTasks = True

        super(
            LearnedFeatureExtractor,
            self).__init__(
            lexicon=list(
                self.lexicon),
            tasks=tasks,
            cuda=cuda,
            H=self.H,
            bidirectional=True)

def main(args):
    """
    Takes the return value of the `commandlineArguments()` function as input and
    trains/tests the model on manipulating sequences of numbers.
    """
    random.seed(args.pop("random_seed"))

    tasks = make_list_bootstrap_tasks()
    print (tasks)
    maxTasks = args.pop("maxTasks")
    if maxTasks and len(tasks) > maxTasks:

        eprint("Unwilling to handle {} tasks, truncating..".format(len(tasks)))
        random.shuffle(tasks)
        del tasks[maxTasks:]

    baseGrammar = Grammar.uniform(McCarthyPrimitives())

    extractor = {
        "learned": LearnedFeatureExtractor,
    }[args.pop("extractor")]
    extractor.H = args.pop("hidden")

    timestamp = datetime.datetime.now().isoformat()
    outputDirectory = "experimentOutputs/list/%s"%timestamp
    os.system("mkdir -p %s"%outputDirectory)
    
    args.update({
        "featureExtractor": extractor,
        "outputPrefix": "%s/list"%outputDirectory,
        "evaluationTimeout": 0.0005,
    })
    
    eprint("Got {} list tasks".format(len(tasks)))
    split = args.pop("split")
    if split:
        train_some = defaultdict(list)
        for t in tasks:
            # necessary = train_necessary(t)
            # if not necessary:
            #     continue
            # if necessary == "some":
            # train_some[t.name.split()[0]].append(t)
            # else:
            t.mustTrain = True
        # for k in sorted(train_some):
        #     ts = train_some[k]
        #     random.shuffle(ts)
        #     ts.pop().mustTrain = True

        test, train = testTrainSplit(tasks, split)

        eprint(
            "Alotted {} tasks for training and {} for testing".format(
                len(train), len(test)))
    else:
        train = tasks
        test = []

    explorationCompression(baseGrammar, train, testingTasks=test, **args)
