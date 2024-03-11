from .EstripAnalysisTool.Estrip import Estrip
import os
from itertools import chain
from typing import Callable, Iterable


class EstripIterator:
    def __init__(self, path: str) -> None:
        self.path = path
        with open(path, 'r') as f:
            self.lines = f.readlines();
        self.ptr = 0

    def __iter__(self):
        return self
    
    def __next__(self)->dict[str, str]:
        # 处理每一行（例如打印）
        for line in self.lines[self.ptr:]:
            self.ptr += 1
            if line.find('FlightData_Plan') != -1:
                try:
                    ep = Estrip(line)
                    return vars(ep)
                except Exception as e:
                    print(f'EstripIterator: {self.path}: Exception raise near line {self.ptr}')
        raise StopIteration()


class DirEstripIterator:
    def __init__(self, dir_path: str) -> None:
        logFiles = os.listdir(dir_path)
        self.iter = chain(*[EstripIterator(os.path.join(dir_path, logFile)) for logFile in logFiles])

    def __iter__(self):
        return self
    
    def __next__(self)->dict[str, str]:
        return next(self.iter)
    

class Unique:
    def __init__(self, iter: Iterable, key: Callable[[Iterable], bool]) -> None:
        self.iter = iter
        self.key = key
        self.keys = set()

    def __iter__(self):
        return self
    
    def __next__(self):
        for item in self.iter:
            k = self.key(item)
            if k not in self.keys:
                self.keys.add(k)
                return item
        raise StopIteration()
    

def bucket_map(iter: Iterable, key: Callable, val: Callable = None)->dict:
    ret = {}
    for item in iter:
        k = key(item)
        if k not in ret:
            ret[k] = []
        ret[k].append(val(item) if val else item)
    return ret
