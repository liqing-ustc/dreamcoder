from dreamcoder.program import Primitive, Program
from dreamcoder.grammar import Grammar
from dreamcoder.type import tlist, tint, tbool, arrow, t0, t1, t2

import math
from functools import reduce

def _if(c): return lambda t: lambda f: t if c else f
def _if0(a): return lambda b: lambda c: b if a == 0 else c

def _eq0(x): return x == 0
# def _eq(x): return lambda y: x == y

def _incr(x): return x + 1
def _decr0(x): return max(0, x - 1)

def _gt(x): return lambda y: x > y

def _positive(x): return x > 0

def _add(x, y): return x + y

def _minus0(x, y): return max(0, x - y)

class RecursionDepthExceeded(Exception):
    pass

def _fix(argument):
    def inner(body):
        recursion_limit = [50]

        def fix(x):
            def r(z):
                recursion_limit[0] -= 1
                if recursion_limit[0] <= 0:
                    raise RecursionDepthExceeded()
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

def McCarthyPrimitives():
    "These are < primitives provided by 1959 lisp as introduced by McCarthy"
    return [
        Primitive("0", tint, 0),
        Primitive("incr", arrow(tint, tint), _incr),
        Primitive("decr0", arrow(tint, tint), _decr0),
        # Primitive("if", arrow(tbool, t0, t0, t0), _if),
        # Primitive("eq0", arrow(tint, tbool), _eq0),
        Primitive("if0", arrow(t0, t0, t0, t0), _if0),
        # primitiveRecursion1,
        primitiveRecursion2,
        # Primitive("gt?", arrow(tint, tint, tbool), _gt),
        # Primitive("positive?", arrow(tint, tbool), _positive),
        # Primitive("+", arrow(tint, tint, tint), _add),
        # Primitive("-0", arrow(tint, tint, tint), _minus0),
    ]


if __name__ == "__main__":
    bootstrapTarget()
    g = Grammar.uniform(McCarthyPrimitives())
    # with open("/home/ellisk/om/ec/experimentOutputs/list_aic=1.0_arity=3_ET=1800_expandFrontier=2.0_it=4_likelihoodModel=all-or-nothing_MF=5_baseline=False_pc=10.0_L=1.0_K=5_rec=False.pickle", "rb") as handle:
    #     b = pickle.load(handle).grammars[-1]
    # print b

    # p = Program.parse(
    #     "(lambda (lambda (lambda (if (empty? $0) empty (cons (+ (car $1) (car $0)) ($2 (cdr $1) (cdr $0)))))))")
    # t = arrow(tlist(tint), tlist(tint), tlist(tint))  # ,tlist(tbool))
    # print(g.logLikelihood(arrow(t, t), p))
    # assert False
    # print(b.logLikelihood(arrow(t, t), p))

    # # p = Program.parse("""(lambda (lambda
    # # (unfold 0
    # # (lambda (+ (index $0 $2) (index $0 $1)))
    # # (lambda (1+ $0))
    # # (lambda (eq? $0 (length $1))))))
    # # """)
    # # p = Program.parse("""(lambda (lambda
    # # (map (lambda (+ (index $0 $2) (index $0 $1))) (range (length $0))  )))""")
    # # # .replace("unfold", "#(lambda (lambda (lambda (lambda (fix1 $0 (lambda (lambda (#(lambda (lambda (lambda (if $0 empty (cons $1 $2))))) ($1 ($3 $0)) ($4 $0) ($5 $0)))))))))").\
    # # # replace("length", "#(lambda (fix1 $0 (lambda (lambda (if (empty? $0) 0 (+ ($1 (cdr $0)) 1))))))").\
    # # # replace("forloop", "(#(lambda (lambda (lambda (lambda (fix1 $0 (lambda (lambda (#(lambda (lambda (lambda (if $0 empty (cons $1 $2))))) ($1 ($3 $0)) ($4 $0) ($5 $0))))))))) (lambda (#(eq? 0) $0)) $0 (lambda (#(lambda (- $0 1)) $0)))").\
    # # # replace("inc","#(lambda (+ $0 1))").\
    # # # replace("drop","#(lambda (lambda (fix2 $0 $1 (lambda (lambda (lambda (if
    # # # (#(eq? 0) $1) $0 (cdr ($2 (- $1 1) $0)))))))))"))
    # # print(p)
    # # print(g.logLikelihood(t, p))
    # # assert False

    # print("??")
    # p = Program.parse(
    #     "#(lambda (#(lambda (lambda (lambda (fix1 $0 (lambda (lambda (if (empty? $0) $3 ($4 (car $0) ($1 (cdr $0)))))))))) (lambda $1) 1))")
    # for j in range(10):
    #     l = list(range(j))
    #     print(l, p.evaluate([])(lambda x: x * 2)(l))
    #     print()
    # print()

    # # print("multiply")
    # # p = Program.parse(
    # #     "(lambda (lambda (lambda (if (eq? $0 0) 0 (+ $1 ($2 $1 (- $0 1)))))))")
    # # print(g.logLikelihood(arrow(arrow(tint, tint, tint), tint, tint, tint), p))
    # # print()

    # print("take until 0")
    # p = Program.parse("(lambda (lambda (if (eq? $1 0) empty (cons $1 $0))))")
    # print(g.logLikelihood(arrow(tint, tlist(tint), tlist(tint)), p))
    # print()

    # # print("countdown primitive")
    # # p = Program.parse(
    # #     "(lambda (lambda (if (eq? $0 0) empty (cons (+ $0 1) ($1 (- $0 1))))))")
    # # print(
    # #     g.logLikelihood(
    # #         arrow(
    # #             arrow(
    # #                 tint, tlist(tint)), arrow(
    # #                 tint, tlist(tint))), p))
    # # print(_fix(9)(p.evaluate([])))
    # # print("countdown w/ better primitives")
    # # p = Program.parse(
    # #     "(lambda (lambda (if (eq0 $0) empty (cons (+1 $0) ($1 (-1 $0))))))")
    # # print(
    # #     g.logLikelihood(
    # #         arrow(
    # #             arrow(
    # #                 tint, tlist(tint)), arrow(
    # #                 tint, tlist(tint))), p))

    # # print()

    # # print("prepend zeros")
    # # p = Program.parse(
    # #     "(lambda (lambda (lambda (if (eq? $1 0) $0 (cons 0 ($2 (- $1 1) $0))))))")
    # # print(
    # #     g.logLikelihood(
    # #         arrow(
    # #             arrow(
    # #                 tint,
    # #                 tlist(tint),
    # #                 tlist(tint)),
    # #             tint,
    # #             tlist(tint),
    # #             tlist(tint)),
    # #         p))
    # # print()
    # # assert False

    # # p = Program.parse(
    # #     "(lambda (fix1 $0 (lambda (lambda (if (empty? $0) 0 (+ 1 ($1 (cdr $0))))))))")
    # # print(p.evaluate([])(list(range(17))))
    # # print(g.logLikelihood(arrow(tlist(tbool), tint), p))

    # # p = Program.parse(
    # #     "(lambda (lambda (if (empty? $0) 0 (+ 1 ($1 (cdr $0))))))")
    # # print(
    # #     g.logLikelihood(
    # #         arrow(
    # #             arrow(
    # #                 tlist(tbool), tint), arrow(
    # #                 tlist(tbool), tint)), p))

    # # p = Program.parse(
    # #     "(lambda (fix1 $0 (lambda (lambda (if (empty? $0) 0 (+ (car $0) ($1 (cdr $0))))))))")

    # # print(p.evaluate([])(list(range(4))))
    # # print(g.logLikelihood(arrow(tlist(tint), tint), p))

    # # p = Program.parse(
    # #     "(lambda (lambda (if (empty? $0) 0 (+ (car $0) ($1 (cdr $0))))))")
    # # print(p)
    # # print(
    # #     g.logLikelihood(
    # #         arrow(
    # #             arrow(
    # #                 tlist(tint),
    # #                 tint),
    # #             tlist(tint),
    # #             tint),
    # #         p))

    # # print("take")
    # # p = Program.parse(
    # #     "(lambda (lambda (lambda (if (eq? $1 0) empty (cons (car $0) ($2 (- $1 1) (cdr $0)))))))")
    # # print(p)
    # # print(
    # #     g.logLikelihood(
    # #         arrow(
    # #             arrow(
    # #                 tint,
    # #                 tlist(tint),
    # #                 tlist(tint)),
    # #             tint,
    # #             tlist(tint),
    # #             tlist(tint)),
    # #         p))
    # # assert False

    # # print(p.evaluate([])(list(range(4))))
    # # print(g.logLikelihood(arrow(tlist(tint), tlist(tint)), p))

    # # p = Program.parse(
    # #     """(lambda (fix (lambda (lambda (match $0 0 (lambda (lambda (+ $1 ($3 $0))))))) $0))""")
    # # print(p.evaluate([])(list(range(4))))
    # # print(g.logLikelihood(arrow(tlist(tint), tint), p))
