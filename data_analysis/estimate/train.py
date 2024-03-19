from scipy.optimize import minimize
from data_analysis.estimate.model import Data
from .model import Model, Data
from .utils import *
import pickle


class TestModel(Model):
    '''参数：[u(pn), s(pn), k(tn)]

    mu(p, t) = u[p] * k[t]

    sigma(p, t) = s[p]
    '''
    def __init__(self, data: list[Data], p_numerizer: Numerizer, t_numerizer: Numerizer) -> None:
        super().__init__(data)
        self.p_numerizer = p_numerizer
        self.t_numerizer = t_numerizer
        self.num_p = len(p_numerizer)
        self.num_t = len(t_numerizer)
        self.num_arg = self.num_p * 2 + self.num_t
        
    def u(self, p: int, t: int, args: list[float]) -> float:
        assert len(args) == self.num_arg
        return args[p] * args[2 * self.num_p + t]

    def u_der(self, p: int, t: int, args: list[float]) -> list[float]:
        assert len(args) == self.num_arg
        d = [0] * self.num_arg
        d[p] = args[2 * self.num_p + t]
        d[2 * self.num_p + t] = args[p]
        return d
    
    def s(self, p: int, t: int, args: list[float]) -> float:
        assert len(args) == self.num_arg
        return args[self.num_p + p]

    def s_der(self, p: int, t: int, args: list[float]) -> list[float]:
        assert len(args) == self.num_arg
        d = [0] * self.num_arg
        d[self.num_p + p] = 1
        return d


if __name__ == '__main__':
    data, p_numerizer, t_numerizer = load_data('data_analysis/result.json')

    model = TestModel(data, p_numerizer, t_numerizer)

    init_args = [1000] * model.num_p + [300] * model.num_p + [1] * model.num_t

    for p in range(model.num_p):
        t = []
        for d in data:
            if d.p == p:
                t.append(d.y)
        init_args[p] = sum(t) / len(t)
    
    # print(init_args)

    # print(model.logL(init_args))
    # print(model.logL_der(init_args))
    # print(model.logL(vec_add(init_args, scalar_mul(1e-3, model.logL_der(init_args)))))

    res = minimize(lambda x: -model.logL(x), 
                   init_args, 
                   method='BFGS', 
                   jac=lambda x: scalar_mul(-1, model.logL_der(x)),
                   options={'gtol': 1e-1, 'disp': True})
    print(res)

    with open('data_analysis/estimate/args.json', 'w') as f:
        json.dump(list(res.x), f)

    with open('data_analysis/estimate/res.pickle', 'wb') as f:
        pickle.dump((model, list(res.x)), f)
