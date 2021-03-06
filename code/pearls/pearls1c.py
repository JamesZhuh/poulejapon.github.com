from itertools import combinations
from collections import defaultdict
from math import ceil, log

def measure(pearl_weights, left, right):
    # returns the result of a measure.
    left_weight = sum(pearl_weights[i] for i in left)
    right_weight = sum(pearl_weights[i] for i in right)
    return cmp(left_weight, right_weight)

def measures(n):
    # generator  yielding all the possible way 
    # to select 2 set of k pearls 
    # to put on the plates of the scale
    for nb_pearls_in_measure in range(1,n/2+1):
        for pearls_involved in combinations(range(n), nb_pearls_in_measure*2):
            pearls_involved_set = set(pearls_involved)
            for left in combinations(pearls_involved, nb_pearls_in_measure):
                right = sorted(pearls_involved_set.difference(left))
                yield (left, right)

def populations_after_measures(population, n):
    # loops on the possible way to make a measure
    # and yield list of the three populations 
    # matching with the 3 possible outcome of 
    # the scale
    branches = []
    for (left, right) in measures(n):
        measure_results = defaultdict(list)
        for configuration in population:
            measure_output = measure(configuration, left, right)
            measure_results[measure_output].append(configuration)
        if len(measure_results) > 1:
            branches.append(measure_results.values())
    return sorted(branches, key=lambda x:max(map(len, x)))


def browse_solutions(population, n):
    for branches in populations_after_measures(population, n):
        yield max(
            solve(branch_population, n)
            for branch_population in branches
        )

def min_with_limit(g, limit):
    res = g.next()
    for x in g:
        res = min(res, x)
        if res<=limit:
            return res
    return res

def solve(population, n):
    if len(population) == 1:
        return 0
    else:
        limit = ceil(log(len(population),3))-1
        solutions = browse_solutions(population, n)
        return 1 + min_with_limit(solutions, limit)

def pearl_cutting_sooner(n):
    if n <= 2:
        return None
    population = []
    for i in range(n):
        pearl_weights = [0] * n
        pearl_weights[i] = 1
        population.append(tuple(pearl_weights))
        pearl_weights[i] = -1 # negative weight haha!
        population.append(tuple(pearl_weights))
    return solve(population, n)
