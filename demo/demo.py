import sys
if "." not in sys.path:
    sys.path.append(".")

import streamlit as st
import pandas as pd
import importlib
from utils import *


data_path = st.radio(
    "选择输入数据",
    ['data/example.csv', 'data/input_sample.csv'])
config = {
    'data/example.csv': {
        'methods': ["不做处理", "按最早可能起飞时间排序", "暴力枚举"],
        'adaptor': None
    },
    'data/input_sample.csv': {
        'methods': ["不做处理", "按最早可能起飞时间排序"],
        'adaptor': default_adaptor
    }
}[data_path]

df = pd.read_csv(data_path, encoding='ANSI')

st.subheader("航班数据")
st.table(df)

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

st.write(f"总延迟：{result['total delay']}")
st.markdown(result["markdown table"])
