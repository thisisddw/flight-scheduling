import sys
if "." not in sys.path:
    sys.path.append(".")

import streamlit as st
import pandas as pd
import importlib
from utils import *


st.set_page_config(
    page_title="交互演示",
    page_icon="✈️",
    # layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("### 航班数据")

data_path = st.sidebar.radio(
    """选择输入数据""",
    ['data/example.csv', 'data/input_sample.csv', '上传文件'])

if data_path == '上传文件':
    uploaded_file = st.file_uploader("选择一个CSV文件（utf-8编码）", type='csv')
    if not uploaded_file:
        st.warning('请上传文件')
        st.stop()
    data_path = 'data/uploaded_file.csv'
    content = uploaded_file.read()
    with open(data_path, 'wb') as f:
        f.write(content)

config = {
    'data/example.csv': {
        'methods': ["按最早可能起飞时间排序", "暴力枚举", "不做处理"],
        'desc': '这是我们按照第一种输入格式编造的简单测试数据。',
        'adaptor': None
    },
    'data/input_sample.csv': {
        'methods': ["按最早可能起飞时间排序", "不做处理"],
        'desc': '来自用户的2024.1.15航班数据。我们按照它的格式设置了第二种输入格式。',
        'adaptor': default_adaptor
    },
    'data/uploaded_file.csv': {
        'methods': ["按最早可能起飞时间排序", "不做处理"],
        'desc': '如果格式错误或编码错误可能会报错。',
        'adaptor': default_adaptor
    }
}[data_path]

st.info(config['desc'])

df = pd.read_csv(data_path, encoding='utf-8')

st.dataframe(df)
# st.table(df)

method = st.sidebar.radio(
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
