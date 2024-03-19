import math
from .utils import *


class Model:
    def __init__(self, data: list[Data]) -> None:
        self.data = data

    def u(self, p: int, t: int, args: list[float]) -> float:
        pass

    def u_der(self, p: int, t: int, args: list[float]) -> list[float]:
        pass
    
    def s(self, p: int, t: int, args: list[float]) -> float:
        pass

    def s_der(self, p: int, t: int, args: list[float]) -> list[float]:
        pass

    def logL(self, args: list[float]) -> float:
        s2_list = [self.s(d.p, d.t, args) ** 2 for d in self.data]
        u_list = [self.u(d.p, d.t, args) for d in self.data]
        y_list = [d.y for d in self.data]
        return -0.5 * sum(math.log(2*math.pi*s2) for s2 in s2_list) \
                - sum(((y - u) ** 2) * 0.5 / s2 for u, s2, y in zip(u_list, s2_list, y_list))
    
    def logL_der(self, args: list[float]) -> list[float]:
        s_list = [self.s(d.p, d.t, args) for d in self.data]
        sd_list = [self.s_der(d.p, d.t, args) for d in self.data]
        u_list = [self.u(d.p, d.t, args) for d in self.data]
        ud_list = [self.u_der(d.p, d.t, args) for d in self.data]
        y_list = [d.y for d in self.data]
        term1 = multi_vec_add(scalar_mul(-1 / s, sd) for s, sd in zip(s_list, sd_list))
        term2 = multi_vec_add(scalar_mul(((y - u) ** 2) / (s ** 3), sd) 
            for y, u, s, sd in zip(y_list, u_list, s_list, sd_list))
        term3 = multi_vec_add(scalar_mul((y - u) / (s ** 2), ud)
                              for y, u, s, ud in zip(y_list, u_list, s_list, ud_list))
        return multi_vec_add([term1, term2, term3])
    