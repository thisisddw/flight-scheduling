from .utils import EstripIterator, DirEstripIterator, Unique
import json


test_path = 'data_analysis/logs/'
# test_path = 'data_analysis/logs/2024030120-Estrip.log'
output_path = 'data_analysis/data.json'

def check_exist(data: dict[str, str], fields: list[str])->bool:
    for f in fields:
        if f not in data or data[f] == '':
            return False
    return True

if __name__ == '__main__':
    it = DirEstripIterator(test_path)
    it = filter(lambda x: check_exist(x, [
        'Time',
        'ACID',
        'AIRCRAFT',
        'DRWY',
        'GATE',
        'TaxiTime'
    ]), it)
    it = Unique(it, lambda x: f'{x["Time"][:8]}-{x["ACID"]}')

    data = list(it)

    with open(output_path, 'w') as f:
        json.dump(data, f)
