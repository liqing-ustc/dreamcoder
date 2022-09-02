try:
    import binutil  # required to import from dreamcoder modules
except ModuleNotFoundError:
    import bin.binutil  # alt import if called as module

from dreamcoder.dreamcoder import commandlineArguments, ecIterator
from dreamcoder.grammar import Grammar
from dreamcoder.program import Primitive
from dreamcoder.task import Task
from dreamcoder.type import arrow, tint, tlist, t0
from dreamcoder.utilities import numberOfCPUs

def _first(x): return [x[0]]

def _append(x): return lambda y: x + y

primitives = [
    Primitive("scan_first", arrow(tlist(t0), tlist(t0)), _first),
    Primitive("scan_append", arrow(tlist(t0), tlist(t0), tlist(t0)), _append),
]

for i in range(7):
	primitives.append(Primitive(f'scan_{i}', arrow(tlist(tint)), [i] if i > 0 else []))

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