from .utils import EstripIterator, DirEstripIterator, Unique
import json
import os
import openpyxl


test_path = 'data_analysis/logs/'
# test_path = 'data_analysis/logs/2024030120-Estrip.log'
output_path = 'data_analysis/data.json'

def check_exist(data: dict[str, str], fields: list[str])->bool:
    for f in fields:
        if f not in data or data[f] == '':
            return False
    return True

def excel_to_dict(filename):
    wb = openpyxl.load_workbook(filename)
    sheet = wb.active

    data = []

    headers = [cell.value for cell in sheet[1]]

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[-1] == ' NNN':
            continue
        row = list(row)
        #print(row)
        for i in range(len(row)):
            row[i] = str(row[i]).strip()
        #print(row)
        row_dict = dict(zip(headers, row))
        data.append(row_dict)
    
    return data

def process_data(file):
    file = filter(lambda x: check_exist(x, [
            'Time',
            'ACID',
            'AIRCRAFT',
            'DRWY',
            'GATE',
            'TaxiTime'
        ]), file)
    file = Unique(file, lambda x: f'{x["Time"][:8]}-{x["ACID"]}')
    return file


if __name__ == '__main__':
    current_dt = os.getcwd()
    excel_path = os.path.join(current_dt, 'data_analysis', 'data', 'data.xlsx')
    it = excel_to_dict(excel_path)
    data = list(process_data(it))
    print(len(data))
    old_data = DirEstripIterator(test_path)
    data = data + list(process_data(old_data))

    seen_plan_id = set()
    print(len(data))
    unique_data = []
    for d in data:
        plan_id = int(d['PlanID'])
        anti_ice = int(d['AREA_DEICING_ID'])
        if plan_id in seen_plan_id:
            continue
        if anti_ice != 0:
            continue
        unique_data.append(d)
        seen_plan_id.add(plan_id)
    print(len(unique_data))
    data = unique_data #flights in unique_data do not contain anti-ice

    with open(output_path, 'w') as f:
        json.dump(data, f)