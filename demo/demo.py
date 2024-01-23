import sys
if "." not in sys.path:
    sys.path.append(".")

import streamlit as st
import pandas as pd
import importlib
from utils import *

data_path = 'example.csv'
df = pd.read_csv(data_path)

st.subheader("航班数据")
st.table(df)

method = st.radio(
    "选择一种方法",
    ["不做处理", "按最早可能起飞时间排序", "暴力枚举"])
module_name = {
    "不做处理": "fcfs", 
    "暴力枚举": "bruteforce", 
    "按最早可能起飞时间排序": "sortbytakeoff",
}


@st.cache_data
def compute(method_name: str, data_path: str):
    solver = importlib.import_module("method." + module_name[method_name])
    return test_method(solver.solve, data_path)


result = compute(method, data_path)

st.markdown(result["markdown table"])
st.write(f"总延迟：{result['total delay']}")
