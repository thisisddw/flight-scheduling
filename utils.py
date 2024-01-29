import json
import csv
import method
from typing import Any, Callable


class PkcGroup:
    def __init__(self, name: str, id_list: str, slip_time: int) -> None:
        self.name = name
        self.slip = slip_time
        self.id_list = []
        if slip_time is None:
            self.slip = 30
            print(f"PkcGroup {name} 的值是null，现在用30代替。")
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


flight_attributes = { 'id', 'type', 'EOBT', 'PKC' }


class InputAdaptor:
    def __init__(self, cast: dict[str,tuple[str,Callable[[str],str]]]) -> None:
        trgs = { t[0] for t in cast.values() }
        assert(trgs == flight_attributes)
        self.cast = cast
        for k in self.cast.keys():
            if self.cast[k][1] is None:
                self.cast[k] = self.cast[k][0], lambda x: x

    def __call__(self, row: dict) -> str:
        new_row = { 'original': row }
        for src, (trg, cast) in self.cast.items():
            new_row[trg] = cast(row[src])
        return new_row


default_adaptor = InputAdaptor({
    '航班号': ('id', None),
    '机型': ('type', lambda x: x[-1] if x != '' else ''),
    'EOBT': ('EOBT', lambda x: x.split(' ')[1] if x != '' else ''),
    '推出机位': ('PKC', None)
})


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


def load_data(path: str, pkcgs: list[PkcGroup], adaptor: InputAdaptor = None):

    def get_slip_time(pkcgs: list[PkcGroup], id: int):
        ret = []
        for pkcg in pkcgs:
            if id in pkcg:
                ret.append(pkcg.slip)
        assert(len(ret) == 1)
        return ret[0]
    
    def check_row_integrity(row: dict):
        for k in flight_attributes:
            if k not in row or row[k] == '':
                return False
        return True

    ret = []
    with open(path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if adaptor:
                row = adaptor(row)
            if not check_row_integrity(row):
                print(f'由于缺少属性{flight_attributes}之一，丢弃一行数据')
                continue            
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
    table  = '|     |id      |type |EOBT |开始滑行|滑行时间|起飞时间|延迟 |\n'
    table += '|-----|--------|-----|-----|--------|--------|--------|-----|\n'

    for i, p in enumerate(perm):
        flight = flights[p]
        ss, to = details[i]['slip start'], details[i]['take off']
        delay = ss - flight["EOBT"]
        row = f"|%-5s|%-8s|%-5s|%-5s|%-8s|%-8s|%-8s|%-5s|\n" % (
            str(i), str(flight["id"]), str(flight["type"]),
            m2hm(flight["EOBT"]), m2hm(ss), str(flight["SLIP"]), m2hm(to), str(delay)
        )
        table += row

    return table


def test_method(solve: Callable, sep: dict, flights: list)->dict:
    perm = solve(flights, sep)
    details, tot_delay = method.schedule_details(flights, sep, perm)

    return {
        'markdown table': markdown_table(flights, perm, details),
        'total delay': tot_delay,
    }
