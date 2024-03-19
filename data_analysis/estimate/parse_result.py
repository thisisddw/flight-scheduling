from .train import *
import pickle

with open('data_analysis/estimate/res.pickle', 'rb') as f:
    (model, args) = pickle.load(f)

ps = model.p_numerizer.s2i.keys()
ts = model.t_numerizer.s2i.keys()

results = {}

def s2ms(x: int)->str:
    assert isinstance(x, int)
    m = x // 60
    s = x % 60
    return f'{m:02d}:{s:02d}'

for p in ps:
    for t in ts:
        key = f'{p}-{t}'
        pid = model.p_numerizer.to_id(p)
        tid = model.t_numerizer.to_id(t)
        val = model.u(pid, tid, args), model.s(pid, tid, args)
        val = s2ms(int(val[0])), s2ms(int(val[1]))
        results[key] = val

# print(len(results))
with open('data_analysis/estimate/readable_result.json', 'w') as f:
    json.dump(results, f)
