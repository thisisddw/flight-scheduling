from utils import *
import importlib


methods_to_test = [
    'fcfs',
    'sortbytakeoff',
    # 'bruteforce',
]

pkcgs, sep = load_config()

if __name__ == '__main__':
    # flights = load_data('data/example.csv', pkcgs)
    flights = load_data('data/input_sample.csv', pkcgs, default_adaptor)
    result = {}
    
    for method in methods_to_test:
        scheduler = importlib.import_module(f'method.{method}')
        result[method] = test_method(scheduler.solve, sep, flights).values()

    for name, (table, delay) in result.items():
        print('## ' + name + '\n')
        print(f"total delay is {delay}m\n")
        print(table)