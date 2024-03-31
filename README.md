## 使用方法

### 数据处理：
```
python -m data_analysis.preprocess  # 读取 logs/ 目录下的文件，清洗数据，同时将data.xlsx放到data目录下，读取后合并去重，产生data.json
python -m data_analysis.main        # 读取data.json，按照 机位-跑道-机型 分组，产生result.json
```

### 训练统计模型
```
python -m data_analysis.estimate.train          # 读取数据处理产生的result.json，产生args.json和res.pickle
python -m data_analysis.estimate.parse_result   # 读取res.pickle，产生readable_result.json
```

### 数据展示：

准备运行环境：

```
python -m venv env
env\Scripts\activate
pip install streamlit
```

首先把result.json和readable_result.json放到demo/目录下，然后
```
streamlit run demo/demo.py          # 产生demo网页
```
