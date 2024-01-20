from itertools import permutations
from . import *

def solve(flights: list, sep: dict):
    n_flight = len(flights)

    if (n_flight >= 10):
        print(f'Warning: Input size is {n_flight}. It may takes a long time to iterate through all the permutations.')

    best_delay = 1e9
    best_perm = list(range(n_flight))

    cnt = 0

    for perm in permutations(list(range(n_flight))):
        _, tot_delay = schedule_details(flights, sep, perm)
        if tot_delay < best_delay:
            best_delay = tot_delay
            best_perm = perm
        # cnt += 1
        # if cnt % 10000 == 0:
        #     print(cnt)

    return best_perm
