import json


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        bars = json.load(f);
        return bars

def get_biggest_bar(data):
    pass


def get_smallest_bar(data):
    pass


def get_closest_bar(data, longitude, latitude):
    pass


if __name__ == '__main__':
    load_data('data.json')
