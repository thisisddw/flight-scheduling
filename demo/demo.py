import sys
if "." not in sys.path:
    sys.path.append(".")

import streamlit as st
import pandas as pd
import json

from data_analysis.main import get_gates_types

@st.cache_data
def get_result()->tuple[dict[str, list[int]], list[str], list[str]]: # result, gates, types
    with open('demo/result.json') as f:
        r = json.load(f)
    g, t = get_gates_types(r)
    def pad(s):
        while len(s) < 4:
            s = '0' + s
        return s
    return r, sorted(g, key = lambda x: pad(x)), sorted(t)

result, gates, types = get_result()

gates_shown = st.multiselect('选择停机位', gates, default=gates)
# types_shown = st.multiselect('选择机型', types, default=types[:5])
type_groups = st.multiselect('选择机型', ['Axxx', 'Bxxx', 'Others'], default=['Axxx'])
def check(x: str)->bool:
    if 'Axxx' in type_groups and x.startswith('A'):
        return True
    if 'Bxxx' in type_groups and x.startswith('B'):
        return True
    if 'Others' in type_groups and (not x.startswith(('A', 'B'))):
        return True
    return False
types_shown = list(filter(check, types))
direction = st.radio(
    "选择跑道方向",
    ["07", "25"]
)
format = st.radio(
    "选择展示格式",
    ['样本数量', '平均值（样本数量）', '平均值, 样本标准差（样本数量）', '最小值, 最大值（样本数量）']
)

def get_str(data: list[int])->str:

    def s2ms(x: int)->str:
        assert isinstance(x, int)
        m = x // 60
        s = x % 60
        return f'{m:02d}:{s:02d}'

    if len(data) != 0:
        mean = int(sum(data) / len(data))
        var = sum([(x - mean) ** 2 for x in data]) / (len(data) - 1) if len(data) > 1 else 0
        sd = int(var ** 0.5)
    if format == '样本数量':
        return str(len(data))
    elif format == '平均值（样本数量）':
        return f'{s2ms(mean)} ({len(data)})' if len(data) else ''
    elif format == '平均值, 样本标准差（样本数量）':
        return f'{s2ms(mean)}, {s2ms(sd)} ({len(data)})' if len(data) else ''
    elif format == '最小值, 最大值（样本数量）':
        return f'{s2ms(min(data))}, {s2ms(max(data))} ({len(data)})' if len(data) else ''
    else:
        raise Exception('Unexpected Format')

df_data = {
    ty : [get_str(result.get(f'{g}-{direction}-{ty}', [])) for g in gates_shown] for ty in types_shown
}

df = pd.DataFrame(df_data, index = gates_shown)
st.dataframe(df)
st.table(df)
