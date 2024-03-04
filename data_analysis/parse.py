def extract_Type_msg(line: str) -> str:
    id = line.find('Type_msg')
    if id == -1:
        raise Exception('Invalid format')
    t = line.find(']', id)
    return line[id: t + 1]


def split(data: list[str], pointer: int) -> tuple[int, int, list[str], list[str]]:
    data_len = len(data)
    while pointer < data_len:
        if data[pointer] == '.' and pointer + 1 < data_len and extract_Type_msg(data[pointer + 1]) == 'Type_msg[0x605f]':
            break
        pointer += 1
    if pointer == data_len:
        return pointer, pointer, None, None
    
    start = pointer
    end = start
    while end < data_len and not data[end].endswith('End..'):
        end += 1
    if end == data_len:
        raise Exception(f'Can not find end symbol at line {start}')
    end += 1
    
    return start, end, data[start + 2: start + 5], data[start + 5: end - 1]


def parse_plan(plan: list[str]) -> dict[str, str]:
    assert len(plan) == 3

    ret = {}

    p = plan[1].find('=')
    while p != -1:
        assert plan[1][p + 1] == '\"'
        
        t = p - 1
        while plan[1][t] != ' ':
            t -= 1
        ret[plan[1][t + 1: p]] = plan[1][p + 2: plan[1].find('\"', p + 2)]

        p = plan[1].find('=', p + 1)

    del ret['Time']

    return ret


def parse_adex(adex: list[str]) -> dict[str, str]:
    if not adex[-1].endswith('].'):
        raise Exception('Unexpected format')
    adex[-1] = adex[-1][:-2]
    s = adex[0].find('-', 8)
    if s != 51:
        raise Exception('Unexpected format')
    adex[0] = adex[0][s:]

    ret = {}

    for line in adex:
        assert line.startswith('-')
        if line.count(' ') == 0:
            ret[line[1:]] = ''
        else:
            p = line.find(' ')
            ret[line[1:p]] = line[p + 1:]

    return ret
