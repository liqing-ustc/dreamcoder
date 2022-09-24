try:
    import binutil  # required to import from dreamcoder modules
except ModuleNotFoundError:
    import bin.binutil  # alt import if called as module

from dreamcoder.domains.hint.main import main, list_options
from dreamcoder.dreamcoder import commandlineArguments
from dreamcoder.utilities import numberOfCPUs

from dreamcoder.program import Primitive, Program, Invented
from dreamcoder.grammar import Grammar
from dreamcoder.type import tlist, tint, tbool, arrow, t0, t1, t2
from functools import reduce

def _if(c): return lambda t: lambda f: t if c else f
def _if0(a): return lambda b: lambda c: b if a == 0 else c

def _eq0(x): return x == 0
# def _eq(x): return lambda y: x == y

def _incr(x): return x + 1
def _decr0(x): return max(0, x - 1)

def _gt(x): return lambda y: x > y

def _positive(x): return x > 0

def _add(x): return lambda y: x + y

def _minus0(x): return lambda y: max(0, x - y)

def _fix(argument):
    def inner(body):
        recursion_limit = [1000]

        def fix(x):
            def r(z):
                recursion_limit[0] -= 1
                if recursion_limit[0] <= 0:
                    raise RecursionError
                else:
                    return fix(z)
            return body(r)(x)
        return fix(argument)

    return inner


def curry(f): return lambda x: lambda y: f((x, y))


def _fix2(a1):
    return lambda a2: lambda body: \
        _fix((a1, a2))(lambda r: lambda n_l: body(curry(r))(n_l[0])(n_l[1]))


primitiveRecursion1 = Primitive("fix1",
                                arrow(t0,
                                      arrow(arrow(t0, t1), t0, t1),
                                      t1),
                                _fix)

primitiveRecursion2 = Primitive("fix2",
                                arrow(t0, t1,
                                      arrow(arrow(t0, t1, t2), t0, t1, t2),
                                      t2),
                                _fix2)


add = Primitive("+", arrow(tint, arrow(tint, tint)), _add)
minus0 = Primitive("-0", arrow(tint, arrow(tint, tint)), _minus0)

"These are < primitives provided by 1959 lisp as introduced by McCarthy"
primitives = [
    Primitive("0", tint, 0),
    Primitive("incr", arrow(tint, tint), _incr),
    Primitive("decr0", arrow(tint, tint), _decr0),
    Primitive("if0", arrow(t0, t0, t0, t0), _if0),
    primitiveRecursion2,
    # Primitive("if", arrow(tbool, t0, t0, t0), _if),
    # Primitive("eq0", arrow(tint, tbool), _eq0),
    # primitiveRecursion1,
    # Primitive("gt?", arrow(tint, tint, tbool), _gt),
    # Primitive("positive?", arrow(tint, tbool), _positive),
    # add,
    # minus0,
]

if __name__ == '__main__':
    args = commandlineArguments(
        enumerationTimeout=200, activation='tanh', iterations=1, recognitionTimeout=3600,
        a=3, maximumFrontier=5, topK=2, pseudoCounts=30.0,
        helmholtzRatio=0.5, structurePenalty=1.,
        CPUs=min(8, numberOfCPUs()),
        extras=list_options)
    args['noConsolidation'] = True
    args['contextual'] = True
    args['biasOptimal'] = True
    args['auxiliaryLoss'] = True
    args['activation'] = "relu"
    args['useDSL'] = False
    main(args)
