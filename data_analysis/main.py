from .utils import *
import json


def hms2sec(time: str)->int:
    h, m, s = [int(x) for x in time.split(':')]
    return h*60*60 + m*60 + s


def get_gates_types(result: dict[str, list[int]])->tuple[list[str], list[str]]:
    tuple_keys = [k.split('-') for k in result.keys()]
    gates = set(t[0] for t in tuple_keys)
    types = set(t[2] for t in tuple_keys)
    return gates, types


if __name__ == '__main__':

    with open('data_analysis/data.json', 'r') as f:
        data = json.load(f)
    print(len(data))

    result = bucket_map(data, lambda x: f'{x["GATE"]}-{x["DRWY"]}-{x["AIRCRAFT"]}', lambda x: hms2sec(x['TaxiTime']))
    with open('data_analysis/result.json', 'w') as f:
        json.dump(result, f)

    gates, types = get_gates_types(result)

    print(len(gates), ':', gates)
    print(len(types), ':', types)
