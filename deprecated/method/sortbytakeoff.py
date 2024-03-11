type_priority = {
    'L': 0,
    'M': 1,
    'H': 2,
    'A380': 3
}
def solve(flights: list, sep: dict):
    perm = list(range(len(flights)))
    return sorted(perm, 
                  key=lambda x: ((flights[x]['EOBT'] + flights[x]['SLIP']), type_priority[flights[x]['type']]))
