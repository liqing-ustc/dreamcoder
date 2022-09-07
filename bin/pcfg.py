try:
    import binutil  # required to import from dreamcoder modules
except ModuleNotFoundError:
    import bin.binutil  # alt import if called as module

from dreamcoder.dreamcoder import commandlineArguments, ecIterator
from dreamcoder.domains.list.listPrimitives import _reverse, _car, _cdr, _single, _append, _cons
from dreamcoder.domains.hint.hintPrimitives import _incr, _decr0
from dreamcoder.grammar import Grammar
from dreamcoder.program import Primitive
from dreamcoder.task import Task
from dreamcoder.type import arrow, tint, tlist, t0, t1, t2
from dreamcoder.utilities import numberOfCPUs

def _multiply10(x): return x * 10

primitives = [
    Primitive("reverse", arrow(tlist(t0), tlist(t0)), _reverse),
    Primitive("empty", tlist(t0), []),
    Primitive("car", arrow(tlist(t0), t0), _car),
    Primitive("cdr", arrow(tlist(t0), tlist(t0)), _cdr),
    Primitive("singleton", arrow(t0, tlist(t0)), _single),
    Primitive("++", arrow(tlist(t0), tlist(t0), tlist(t0)), _append),
    Primitive("cons", arrow(t0, tlist(t0), tlist(t0)), _cons),
    Primitive("0", tint, 0),
    Primitive("incr", arrow(tint, tint), _incr),
    Primitive("*10", arrow(tint, tint), _multiply10),
]


if __name__ == "__main__":

    args = commandlineArguments(
        enumerationTimeout=200, activation='tanh', iterations=1, recognitionTimeout=3600,
        a=3, maximumFrontier=5, topK=2, pseudoCounts=30.0,
        helmholtzRatio=0.5, structurePenalty=1.,
        CPUs=min(8, numberOfCPUs()))
    args['noConsolidation'] = True
    args['contextual'] = True
    args['biasOptimal'] = True
    args['auxiliaryLoss'] = True
    args['activation'] = "relu"
    args['useDSL'] = False


    # Create grammar

    grammar = Grammar.uniform(primitives)