from record import *


output = 'data_analysis/output.txt'

with open(output, 'w') as f:
    ACID_records = {}
    for r in Unique(DirRecordIterator('data_analysis/log_data/')):
        id = r.plan['ACID']
        if id not in ACID_records.keys():
            ACID_records[id] = []
        ACID_records[id].append(r)
        
    for k,v in ACID_records.items():
        f.write(f'{k}: {len(v)}\n')
