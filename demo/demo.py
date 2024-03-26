import sys
if "." not in sys.path:
    sys.path.append(".")

import streamlit as st
import pandas as pd
import json
from typing import Union

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

@st.cache_data
def get_model_readable_result()->dict[str, list[str]]:  # format: {"{gate}-{dway}-{type}": ["{mean}", "{sigma}"]}
    with open('demo/readable_result.json') as f:
        r = json.load(f)
    return r

result, gates, types = get_result()
model_result = get_model_readable_result()

gate_groups = ['0-49', '50-99', '100-149', 'others']
gate_groups = st.multiselect('选择停机位', gate_groups, default=gate_groups)
def check(x: str)->bool:
    int_x = None
    try:
        int_x = int(x)
    except ValueError:
        pass
    type = 'others'
    if int_x and 0 <= int_x <= 49:
        type = '0-49'
    if int_x and 50 <= int_x <= 99:
        type = '50-99'
    if int_x and 100 <= int_x <= 149:
        type = '100-149'
    return type in gate_groups
gates_shown = list(filter(check, gates))

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
    "选择展示内容",
    [
        '样本数量', 
        '平均值（样本数量）', 
        '平均值, 样本标准差（样本数量）', 
        '最小值, 最大值（样本数量）', 
        '统计模型结果（平均值, 标准差）'
    ]
)

def get_str(data: list[Union[int, str]])->str:

    if format == '统计模型结果（平均值, 标准差）':
        return f'{data[0]}, {data[1]}' if len(data) else ''

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
    ty : [get_str((result if format != '统计模型结果（平均值, 标准差）' else model_result)
                .get(f'{g}-{direction}-{ty}', [])) for g in gates_shown] 
    for ty in types_shown
}

df = pd.DataFrame(df_data, index = gates_shown)
st.dataframe(df)
st.table(df)
