from utils import *
import importlib


methods_to_test = [
    'fcfs',
    'sortbytakeoff',
    'bruteforce',
]

if __name__ == '__main__':
    result = {}
    
    for method in methods_to_test:
        scheduler = importlib.import_module(f'method.{method}')
        result[method] = test_method(scheduler.solve, 'example.csv').values()

    for name, (table, delay) in result.items():
        print('## ' + name)
        print()
        print(f"total delay is {delay}m")
        print()
        print(table)