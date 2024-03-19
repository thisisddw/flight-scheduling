from typing import Iterable
import json


class Data:
    def __init__(self, p: int, t: int, y: float) -> None:
        self.p = p
        self.t = t
        self.y = y


class Numerizer:
    def __init__(self, data: Iterable[str]) -> None:
        self.s2i = {}
        self.i2s = {}
        for d in data:
            if d not in self.s2i:
                self.s2i[d] = len(self.s2i)
                self.i2s[self.s2i[d]] = d

    def to_id(self, s: str) -> int:
        return self.s2i[s]
    
    def to_str(self, id: int) -> str:
        return self.i2s[id]
    
    def __len__(self) -> int:
        return len(self.s2i)


def load_data(path: str) -> tuple[list[Data], Numerizer, Numerizer]:
    with open(path, 'r') as f:
        datas = json.load(f)    
    
    def get_p_t(key: str) -> tuple[str, str]:
        substrs = key.split('-')
        assert len(substrs) == 3
        return f'{substrs[0]}-{substrs[1]}', substrs[2]

    ps = [get_p_t(k)[0] for k in datas.keys()]
    ts = [get_p_t(k)[1] for k in datas.keys()]

    p_numerizer = Numerizer(ps)
    t_numerizer = Numerizer(ts)

    data = []
    for k, v in datas.items():
        p, t = get_p_t(k)
        for y in v:
            data.append(Data(p_numerizer.to_id(p), t_numerizer.to_id(t), y))

    return data, p_numerizer, t_numerizer


def vec_add(x: list, y: list) -> list:
    assert len(x) == len(y)
    return [s + t for s, t in zip(x, y)]


def multi_vec_add(vecs: Iterable[list]) -> list:
    res = None
    for v in vecs:
        res = v if res == None else vec_add(res, v)
    return res


def scalar_mul(x: float, y: list) -> list:
    return [x * t for t in y]