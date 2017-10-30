import json
import io

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

def read_bytes(byte_arr):
    
    convert = lambda a : a.decode('utf-8')
    lines = list( map(convert, io.BytesIO(byte_arr).read().splitlines()))
    return lines

def get_parsed_file(byte_arr, delimiter):
    data = read_bytes(byte_arr)

    result = {
        'columns': get_columns(data, delimiter),
        'data': get_data(data, delimiter),
    }
    result['data_json'] = json.dumps(result['data'])
    return result
