import json

def read_file(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file]
        return lines

def get_columns(lines, delimiter):
    return lines[0].split(delimiter)

def get_data(lines, delimiter):
    data = []
    
    iterator = iter(lines)
    next(iterator) # skip first line with header

    for line in iterator:
        data.append(line.split(delimiter))

    return data

def get_parsed_file(filename, delimiter):
    data = read_file(filename)

    result = {
        'columns': get_columns(data, delimiter),
        'data': get_data(data, delimiter),
    }
    result['data_json'] = json.dumps(result['data'])
    print(result['data_json'])
    return result
