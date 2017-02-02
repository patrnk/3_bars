import json


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        bars = json.load(f);
        return bars


def get_biggest_bar(data):
    biggest_bar = data[0]
    for bar in data:
        if bar['SeatsCount'] > biggest_bar['SeatsCount']:
            biggest_bar = bar
    return biggest_bar


def get_smallest_bar(data):
    smallest_bar = data[0]
    for bar in data:
        if bar['SeatsCount'] < smallest_bar['SeatsCount']:
            smallest_bar = bar
    return smallest_bar


def get_closest_bar(data, longitude, latitude):
    pass


if __name__ == '__main__':
    print(get_smallest_bar(load_data('data.json'))['Name'])
