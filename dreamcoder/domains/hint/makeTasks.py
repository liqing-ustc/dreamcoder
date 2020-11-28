

from dreamcoder.type import *
from dreamcoder.task import Task
from dreamcoder.utilities import eprint, hashable

from random import randint, random, seed
from itertools import product
import math

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
    # def _div(x, y): return x // y
    def _div(x, y): return math.ceil(x / y)
    _fac = lambda x: math.factorial(x) if x <=20 else None

    n_sample = 20
    noise = 0.
    operatorBootstrap = []

    operatorBootstrap = [
        # Task ("add", arrow(tint, tint, tint),
        #      generate_noise(n_sample*noise) + 
        #      [((a, b), _add(a,b)) for a, b in zip(randomList(len=n_sample*(1-noise)), randomList(len=n_sample*(1-noise)))]),
        # Task ("minus", arrow(tint, tint, tint),
        #      generate_noise(n_sample*noise) + 
        #      [((a, b), _minus(a,b)) for a, b in zip(randomList(len=n_sample*(1-noise)), randomList(len=n_sample*(1-noise)))]),
        # Task ("multiply", arrow(tint, tint, tint),
        #      generate_noise(n_sample*noise) + 
        #      [((a, b), _mul(a,b)) for a, b in zip(randomList(len=n_sample*(1-noise)), randomList(len=n_sample*(1-noise)))]),
        # Task ("divide", arrow(tint, tint, tint),
        #      generate_noise(n_sample*noise) + 
        #      [((a, b), _div(a,b)) for a, b in zip(randomList(len=n_sample*(1-noise)), randomList(minValue=1, len=n_sample*(1-noise)))]),
        Task ("factorial", arrow(tint, tint),
             generate_noise(n_sample*noise, arity=1) + 
             [((a,), _fac(a)) for a in randomList(len=n_sample*(1-noise))]),
    ]

    # # Add counting task
    # from collections import Counter
    # for i in range(10):
    #     task = Task(str(i), arrow(tint),
    #          generate_noise(n_sample*noise, arity=0) + [((), i)] * int(n_sample- n_sample * noise))
    #     ys = [y for _, y in task.examples]
    #     print(i, Counter(ys).most_common(3))
    #     operatorBootstrap.append(task)

    import json
    # tasks = json.load(open('../../outputs/tasks.json'))
    # for i, t in enumerate(tasks):
    #     task = Task(str(i), arrow(tint, tint, tint), t)
    #     operatorBootstrap.append(task)
    # task = Task(str(len(tasks)), arrow(tint, tint, tint), [x for t in tasks for x in t])
    # operatorBootstrap.append(task)

#     examples = {((1, 4), 4): 4, ((3, 2), 6): 4, ((1, 8), 8): 3, ((8, 9), 72): 3, ((7, 8), 56): 3, ((1, 6), 6): 3, ((7, 6), 42): 3, ((6, 1), 6): 2, ((3, 4), 12): 2, ((1, 9), 9): 2, ((8, 4), 32)
# : 2, ((7, 1), 7): 2, ((1, 2), 2): 2, ((6, 8), 48): 2, ((1, 7), 7): 2, ((9, 7), 63): 2, ((1, 3), 3): 2, ((4, 8), 32): 2, ((3, 7), 21): 2, ((2, 4), 4): 1, ((5, 8), 40): 1, ((5, 5), 25): 1, ((8, 6), 48): 1, ((5, 1), 5): 1, ((6, 5), 30
# ): 1, ((9, 9), 81): 1, ((0, 6), 6): 1, ((2, 5), 10): 1, ((2, 7), 14): 1, ((8, 7), 56): 1, ((4, 7), 49): 1, ((9, 5), 45): 1, ((5, 9), 45): 1, ((2, 9), 18): 1, ((4, 9), 36): 1, ((6, 4), 24): 1, ((4, 1), 4): 1, ((6, 2), 6): 1, ((1, 1)
# , 1): 1, ((0, 9), 9): 1, ((2, 2), 2): 1, ((9, 6), 54): 1, ((9, 1), 81): 1, ((6, 3), 24): 1, ((7, 7), 49): 1, ((1, 5), 5): 1, ((3, 5), 15): 1, ((6, 6), 36): 1, ((8, 2), 8): 1, ((9, 3), 45): 1, ((4, 4), 6): 1, ((8, 1), 6): 1, ((5, 6)
# , 30): 1, ((0, 4), 4): 1, ((9, 8), 64): 1, ((6, 7), 42): 1, ((2, 8), 16): 1, ((8, 8), 40): 1, ((0, 8), 8): 1, ((5, 3), 54): 1, ((2, 1), 2): 1, ((9, 4), 6): 1, ((6, 0), 5): 1, ((5, 7), 35): 1, ((9, 2), 3): 1, ((7, 3), 21): 1, ((6, 9
# ), 54): 1, ((3, 9), 10): 1, ((7, 9), 81): 1, ((8, 3), 6): 1, ((2, 0), 14): 1, ((5, 4), 6): 1}
#     examples = {((1, 4), 4): 4, ((3, 2), 6): 4, ((1, 8), 8): 3, ((8, 9), 72): 3, ((7, 8), 56): 3, ((1, 6), 6): 3, ((7, 6), 42): 3, ((6, 1), 6): 2, ((3, 4), 12): 2, ((1, 9), 9): 2, ((8, 4), 32)
# : 2, ((7, 1), 7): 2, ((1, 2), 2): 2, ((6, 8), 48): 2, ((1, 7), 7): 2, ((9, 7), 63): 2, ((1, 3), 3): 2, ((4, 8), 32): 2, ((3, 7), 21): 2, ((2, 4), 4): 1, ((5, 8), 40): 1, ((5, 5), 25): 1, ((8, 6), 48): 1, ((5, 1), 5): 1, ((6, 5), 30
# ): 1, ((9, 9), 81): 1, ((0, 6), 0): 0, ((2, 5), 10): 1, ((2, 7), 14): 1, ((8, 7), 56): 1, ((4, 7), 49): 1, ((9, 5), 45): 1, ((5, 9), 45): 1, ((2, 9), 18): 1, ((4, 9), 36): 1, ((6, 4), 24): 1, ((4, 1), 4): 1, ((6, 2), 6): 1, ((1, 1)
# , 1): 1, ((0, 9), 0): 0, ((2, 2), 2): 1, ((9, 6), 54): 1, ((9, 1), 81): 1, ((6, 3), 24): 1, ((7, 7), 49): 1, ((1, 5), 5): 1, ((3, 5), 15): 1, ((6, 6), 36): 1, ((8, 2), 8): 1, ((9, 3), 45): 1, ((4, 4), 6): 1, ((8, 1), 6): 1, ((5, 6)
# , 30): 1, ((4, 0), 0): 0, ((9, 8), 64): 1, ((6, 7), 42): 1, ((2, 8), 16): 1, ((8, 8), 40): 1, ((8, 0), 0): 0, ((5, 3), 54): 1, ((2, 1), 2): 1, ((9, 4), 6): 1, ((6, 0), 5): 1, ((5, 7), 35): 1, ((9, 2), 3): 1, ((7, 3), 21): 1, ((6, 9
# ), 54): 1, ((3, 9), 10): 1, ((7, 9), 81): 1, ((8, 3), 6): 1, ((2, 0), 14): 1, ((5, 4), 6): 1}
#     examples = [[e]*count for e, count in examples.items()]
#     examples = [y for x in examples for y in x]
#     task = Task("11", arrow(tint, tint, tint), examples)
#     operatorBootstrap.append(task)

    # examples = {((1, 7), 7): 9, ((1, 4), 4): 9, ((7, 3), 21): 8, ((1, 2), 2): 7, ((7, 9), 63): 7, ((8, 9), 72): 7, ((3, 9), 27): 7, ((1, 9), 9): 6, ((0, 4), 4): 6, ((1, 3), 3): 6, ((1, 8), 8): 5, ((1, 1), 1): 5, ((4, 9), 36): 5, ((2, 9), 18): 5, ((1, 6), 6): 5, ((5, 4), 20): 5, ((5, 2), 10): 5, ((0, 1), 1): 4, ((5, 9), 45): 4, ((6, 7), 42): 3, ((1, 5), 5): 3, ((3, 3), 9): 3, ((9, 5), 45): 3, ((6, 9), 54): 3, ((9, 9), 81): 3, ((7, 8), 56): 3, ((9, 8), 72): 2, ((3, 7), 21): 2, ((8, 8), 64): 2, ((3, 6), 18): 2, ((3, 5), 15): 2, ((9, 2), 18): 2, ((4, 5), 20): 2, ((0, 5), 5): 2, ((0, 7), 7): 2, ((9, 4), 36): 2, ((6, 6), 36): 2, ((9, 3), 27): 2, ((7, 5), 35): 2, ((2, 5), 14): 1, ((7, 6), 48): 1, ((8, 5), 40): 1, ((2, 1), 7): 1, ((3, 4), 12): 1, ((0, 3), 3): 1, ((9, 7), 63): 1, ((9, 6), 54): 1, ((0, 8), 8): 1, ((5, 6), 18): 1, ((6, 2), 6): 1, ((9, 0), 27): 1, ((1, 0), 0): 1, ((3, 1), 6): 1, ((8, 1), 20): 1, ((4, 6), 16): 1, ((8, 6), 30): 1, ((4, 7), 49): 1, ((6, 5), 30): 1, ((6, 8), 16): 1, ((0, 9), 9): 1, ((0, 6), 6): 1, ((8, 2), 4): 1, ((2, 8), 4): 1, ((7, 7), 49): 1, ((3, 8), 64): 1, ((3, 2), 6): 1}
    # examples = [[e]*count for e, count in examples.items()]
    # examples = [y for x in examples for y in x]
    # task = Task("12", arrow(tint, tint, tint), examples)
    # operatorBootstrap.append(task)

    # examples = {((6, 4), 24): 8, ((8, 3), 24): 7, ((8, 7), 56): 6, ((6, 8), 48): 6, ((4, 2), 8): 5, ((5, 2), 8): 1, ((4, 7), 32): 1, ((0, 6), 0): 1, ((4, 3), 24): 1, ((4, 0), 8): 1}
    # examples = [[e]*count for e, count in examples.items()]
    # examples = [y for x in examples for y in x]
    # task = Task("14", arrow(tint, tint, tint), examples)
    # operatorBootstrap.append(task)

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