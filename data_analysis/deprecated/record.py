from typing import Union, TextIO, Iterable
from io import TextIOBase
from . import parse
from pathlib import Path
from itertools import chain


class Record:
    def __init__(self, plan: dict[str, str], adex: dict[str, str]) -> None:
        self.plan = plan
        self.adex = adex

    def __str__(self) -> str:
        return str(vars(self))
    
    def strip(self):
        ret = Record({}, {})
        for k,v in self.plan.items():
            if v != '':
                ret.plan[k] = v
        for k,v in self.adex.items():
            if v != '':
                ret.adex[k] = v
        return ret


class RecordIterator:
    def __init__(self, file: Union[str, TextIO]) -> None:
        if isinstance(file, str):
            with open(file, 'r') as f:
                self.lines = f.readlines()
        elif isinstance(file, TextIOBase):
            self.lines = file.readlines()
        else:
            raise ValueError(f'Invalid input type {str(type(file))}')
        
        for i in range(len(self.lines)):
            self.lines[i] = self.lines[i].strip()

        self.pointer = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.pointer < len(self.lines):
            try:
                start, end, plan, adex = parse.split(self.lines, self.pointer)
                self.pointer = end
                if start < len(self.lines):
                    return Record(
                            parse.parse_plan(plan), 
                            parse.parse_adex(adex)
                        )
            except Exception as err:
                raise Exception(f'Exception {type(err)} raised near line {self.pointer}')
                
        raise StopIteration()


class DirRecordIterator:
    def __init__(self, dir: str) -> None:
        directory_path = Path(dir)
        file_list = [f for f in directory_path.iterdir() if f.is_file()]
        self.iter = chain(*[RecordIterator(str(f)) for f in file_list])

    def __iter__(self):
        return self
    
    def __next__(self):
        return self.iter.__next__()


class Unique:
    def __init__(self, iter: RecordIterator) -> None:
        self.iter = iter
        self.set = set()

    def __iter__(self):
        return self
    
    def __next__(self):
        t = self.iter.__next__()
        while str(t) in self.set:
            t = self.iter.__next__()
        self.set.add(str(t))
        return t


def to_df_data(records: list[Record], ARCIDs: list[str], fields: list[str], default_val: str = '') -> tuple[dict, list]:
    df_data = {}
    valid_records = sorted([r for r in records if r.adex['ARCID'] in ARCIDs], key=lambda r: r.adex['ARCID'])
    for f in fields:
        row = [(r.adex[f] if f in r.adex and r.adex[f] != '' else default_val) for r in valid_records]
        df_data[f] = row
    return df_data, [r.adex['ARCID'] for r in valid_records]
