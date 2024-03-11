import os 
from Estrip import Estrip

logFilesPath = "LogFiles"
logFiles = os.listdir(logFilesPath)

resultFile = "resultFile.csv"
with open (resultFile,'w',encoding='utf-8') as resFile:
    resFile.write(f"Time; PlanID; ACID; AIRCRAFT; DRWY; ARWY; GATE; ATPUS; ATLIN; CTOT; COBT; \n")

    # 遍历文件名
    for logFile in logFiles:
        # 拼接文件路径
        logPath = os.path.join(logFilesPath, logFile)

        print(logFile)

        # 打开文件
        with open(logPath, 'r', encoding='utf-8') as file:
            # 读取文件的每一行
            lines = file.readlines()

            # 处理每一行（例如打印）
            for line in lines:
                if line.find('FlightData_Plan') != -1:
                    try:
                        ep = Estrip(line)
                        # ep.printEstrip(False)
                        epline = ep.getEstrip()
                        resFile.write(f"{epline}\n")
                    except Exception as e:
                        print(e)
                        print(line)

