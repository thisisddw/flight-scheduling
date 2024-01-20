import csv
import method


def load_sep():
    ret = {}
    types = ['A380', 'H', 'M', 'L']
    with open('config/sep.csv', 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ty = row['type']
            ret[ty] = {}
            for k in types:
                ret[ty][k] = int(row[k])
    return ret


def load_data(path: str):
    ret = []
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            substr = row['EOBT'].split(':')
            h, m = int(substr[0]), int(substr[1])
            row['EOBT'] = h*60 + m
            row['SLIP'] = int(row['SLIP'])
            ret.append(row)
    return ret


def m2hm(t: int)->str:
    m = str(t % 60)
    return f'{t // 60}:{"0" + m if len(m) < 2 else m}'


def markdown_table(flights, perm, details):
    table = '|     |id   |type |EOBT |开始滑行|滑行时间|起飞时间|延迟 |\n'

    for i, p in enumerate(perm):
        flight = flights[p]
        ss, to = details[i]['slip start'], details[i]['take off']
        delay = ss - flight["EOBT"]
        row = f"|%-5s|%-5s|%-5s|%-5s|%-8s|%-8s|%-8s|%-5s|\n" % (
            str(i), str(flight["id"]), str(flight["type"]),
            m2hm(flight["EOBT"]), m2hm(ss), str(flight["SLIP"]), m2hm(to), str(delay)
        )
        table += row

    return table


def test_method(solve: callable, data_path: str)->dict:
    sep = load_sep()
    flights = load_data(data_path)
    
    perm = solve(flights, sep)
    details, tot_delay = method.schedule_details(flights, sep, perm)

    return {
        'markdown table': markdown_table(flights, perm, details),
        'total delay': tot_delay,
    }
