import sys
if "." not in sys.path:
    sys.path.append(".")

import streamlit as st
import pandas as pd
import importlib
from utils import *
from description import description

st.markdown(description)

st.markdown("## 交互演示")

st.markdown("### 航班数据")

data_path = st.radio(
    """选择输入数据。选项一是编造的简单测试数据，选项二是2024.1.15的航班数据。
    上传文件现在只支持选项二格式的csv文件，而且必须是utf-8编码。""",
    ['data/example.csv', 'data/input_sample.csv', '上传文件'])

if data_path == '上传文件':
    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
    if not uploaded_file:
        st.warning('请上传文件')
        st.stop()
    data_path = 'data/uploaded_file.csv'
    content = uploaded_file.read()
    with open(data_path, 'wb') as f:
        f.write(content)

config = {
    'data/example.csv': {
        'methods': ["不做处理", "按最早可能起飞时间排序", "暴力枚举"],
        'adaptor': None
    },
    'data/input_sample.csv': {
        'methods': ["不做处理", "按最早可能起飞时间排序"],
        'adaptor': default_adaptor
    },
    'data/uploaded_file.csv': {
        'methods': ["不做处理", "按最早可能起飞时间排序"],
        'adaptor': default_adaptor
    }
}[data_path]

df = pd.read_csv(data_path, encoding='utf-8')

st.dataframe(df)
# st.table(df)

method = st.radio(
    "选择一种方法",
    config['methods'])
module_name = {
    "不做处理": "fcfs", 
    "暴力枚举": "bruteforce", 
    "按最早可能起飞时间排序": "sortbytakeoff",
}


@st.cache_data
def compute(method_name: str, data_path: str):
    pkcgs, sep = load_config()
    flights = load_data(data_path, pkcgs, config['adaptor'])
    solver = importlib.import_module("method." + module_name[method_name])
    return test_method(solver.solve, sep, flights)


result = compute(method, data_path)

st.markdown("### 程序输出")

st.write(f"总延迟：{result['total delay']}")
# st.markdown(result["markdown table"])
st.dataframe(result['dataframe'])
