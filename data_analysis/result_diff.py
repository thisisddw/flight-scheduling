import json
import statistics


def get_model_readable_result()->dict[str, list[str]]:  # format: {"{gate}-{dway}-{type}": ["{mean}", "{sigma}"]}
    with open('demo/readable_result.json') as f:
        r = json.load(f)
    return r


def get_data(data, type, start, end):
    result = []
    for _ in range(start, end+1):
        key_str = str(_) + '-25-' + type
        if key_str in data:
            list = data[key_str][0].split(':')
            list = [int(item) for item in list]
            result.append(int(list[0] * 60 + list[1]))
    return result


model_result = get_model_readable_result() # format: {"{gate}-{dway}-{type}": ["{mean}", "{sigma}"]}

result_A20N = get_data(model_result, "A20N", 1, 17)
result_B738 = get_data(model_result, "B738", 6, 45)
result_E190 = get_data(model_result, "E190", 1, 5)

print(statistics.stdev(result_A20N))
print(statistics.stdev(result_B738))
print(statistics.stdev(result_E190))
