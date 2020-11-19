

from dreamcoder.type import *
from dreamcoder.task import Task
from dreamcoder.utilities import eprint, hashable

from random import randint, random, seed
from itertools import product

def make_list_bootstrap_tasks():
    seed(42)

    def suffixes(l):
        if l == []:
            return []
        else:
            return [l[1:]] + suffixes(l[1:])

    def randomList(minValue=0, maxValue=9, len=1):
        return [randint(minValue, maxValue) for _ in range(int(len))]

    def generate_noise(n, arity=2):
        n = int(n)
        xs = []
        for _ in range(arity):
            xs.append(randomList(len=n))
        y = randomList(len=n)
        if arity == 0:
            return [((), s) for s in y]
        return list(zip(zip(*xs), y))

    # Functions to be learnt
    def _add(x, y): return x + y
    def _minus(x, y): return max(0, x - y)
    # def _minus(x, y): return x - y
    def _mul(x, y): return x * y
    def _div(x, y): return x // y

    n_sample = 20
    noise = 0.8

    operatorBootstrap = [
        Task ("add", arrow(tint, tint, tint),
             generate_noise(n_sample*noise) + 
             [((a, b), _add(a,b)) for a, b in zip(randomList(len=n_sample*(1-noise)), randomList(len=n_sample*(1-noise)))]),
        Task ("minus", arrow(tint, tint, tint),
             generate_noise(n_sample*noise) + 
             [((a, b), _minus(a,b)) for a, b in zip(randomList(len=n_sample*(1-noise)), randomList(len=n_sample*(1-noise)))]),
        Task ("multiply", arrow(tint, tint, tint),
             generate_noise(n_sample*noise) + 
             [((a, b), _mul(a,b)) for a, b in zip(randomList(len=n_sample*(1-noise)), randomList(len=n_sample*(1-noise)))]),
        Task ("divide", arrow(tint, tint, tint),
             generate_noise(n_sample*noise) + 
             [((a, b), _div(a,b)) for a, b in zip(randomList(len=n_sample*(1-noise)), randomList(minValue=1, len=n_sample*(1-noise)))]),
    ]

    # Add counting task
    from collections import Counter
    for i in range(10):
        task = Task(str(i), arrow(tint),
             generate_noise(n_sample*noise, arity=0) + [((), i)] * int(n_sample- n_sample * noise))
        ys = [y for _, y in task.examples]
        print(i, Counter(ys).most_common(3))
        operatorBootstrap.append(task)

    return operatorBootstrap


def exportTasks():
    import sys
    import pickle as pickle

    n_examples = 15
    if len(sys.argv) > 1:
        n_examples = int(sys.argv[1])

    eprint("Downloading and generating dataset")
    tasks = sorted(make_list_tasks(n_examples), key=lambda t: t.name)
    eprint("Got {} list tasks".format(len(tasks)))

    with open("data/list_tasks.pkl", "w") as f:
        pickle.dump(tasks, f)
    eprint("Wrote list tasks to data/list_tasks.pkl")