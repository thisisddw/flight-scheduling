import json
import csv
import method


class PkcGroup:
    def __init__(self, name: str, id_list: str, slip_time: int) -> None:
        self.name = name
        self.slip = slip_time
        self.id_list = []
        for s in id_list.split(" "):
            r = [int(_) for _ in s.split("-")]
            if len(r) == 1:
                self.id_list.append((r[0], r[0]))
            else:
                assert(len(r) == 2)
                self.id_list.append((r[0], r[1]))
    
    def __contains__(self, pkc_id: int):
        for l, r in self.id_list:
            if pkc_id >= l and pkc_id <= r:
                return True
        return False


def load_config():
    pkc = []
    with open("config/pkcg.json") as f:
        for [n, id, slip] in json.load(f):
            pkc.append(PkcGroup(n, id, slip))

    sep = {}
    types = ['A380', 'H', 'M', 'L']
    with open('config/sep.csv', 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ty = row['type']
            sep[ty] = {}
            for k in types:
                sep[ty][k] = int(row[k])

    return pkc, sep


def load_data(path: str, pkcgs: list[PkcGroup]):

    def get_slip_time(pkcgs: list[PkcGroup], id: int):
        ret = []
        for pkcg in pkcgs:
            if id in pkcg:
                ret.append(pkcg.slip)
        assert(len(ret) == 1)
        return ret[0]

    ret = []
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            substr = row['EOBT'].split(':')
            h, m = int(substr[0]), int(substr[1])
            row['EOBT'] = h*60 + m
            row['SLIP'] = get_slip_time(pkcgs, int(row['PKC']))
            ret.append(row)
    return ret


def m2hm(t: int)->str:
    m = str(t % 60)
    return f'{t // 60}:{"0" + m if len(m) < 2 else m}'


def markdown_table(flights: list, perm: list, details: list):
    table  = '|     |id   |type |EOBT |开始滑行|滑行时间|起飞时间|延迟 |\n'
    table += '|-----|-----|-----|-----|--------|--------|--------|-----|\n'

    for i, p in enumerate(perm):
        flight = flights[p]
        ss, to = details[i]['slip start'], details[i]['take off']
        delay = ss - flight["EOBT"]
        row = f"|%-5s|%-5s|%-5s|%-5s|%-8s|%-8s|%-8s|%-5s|\n" % (
            str(i), str(flight["id"]), str(flight["type"]),
            m2hm(flight["EOBT"]), m2hm(ss), str(flight["SLIP"]), m2hm(to), str(delay)
        )
        table += row

    return table


def test_method(solve: callable, sep: dict, flights: list)->dict:
    perm = solve(flights, sep)
    details, tot_delay = method.schedule_details(flights, sep, perm)

    return {
        'markdown table': markdown_table(flights, perm, details),
        'total delay': tot_delay,
    }
