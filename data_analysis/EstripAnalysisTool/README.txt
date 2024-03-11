本工具用于解析电子进程单日志数据。

1、将需要解析的文件（例如：2024030201-Estrip.log）放入LogFiles文件夹，可以放入多个文件。
2、运行Main.py得到resultFile.csv。
3、打开resultFile.csv，单元格格式选择数字，并对第一列分列，分隔符为“；”。
4、对“Time”列排序
5、resultFile.csv格式：Time; PlanID; ACID; AIRCRAFT; DRWY; ARWY; GATE; ATPUS; ATLIN; CTOT; COBT。
6、每一行数据未去重。