## 运行环境

- python 3.11

## 运行方法

```
python main.py
```

## 代码结构

```
.
├── config
│   └── sep.csv         # 设置安全间隔
├── example.csv         # 一个航班样例
├── main.py             # 程序入口
├── method              # 用于测试的各种方法
│   ├── __init__.py
│   ├── bruteforce.py
│   ├── fcfs.py
│   └── sortbytakeoff.py
├── README.md
└── utils.py
```

### 输入格式

参考example.csv和utils.py的load_data函数