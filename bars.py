import sys
import json
from math import sqrt


class Bar:

    def __init__(self, json_data):
        self.seat_count = json_data['SeatsCount']
        self.longitude = float(json_data['Longitude_WGS84'])
        self.latitude = float(json_data['Latitude_WGS84'])
        self.name = json_data['Name']

    def distance_to(self, longitude, latitude):
        x2 = (longitude - self.longitude) ** 2
        y2 = (latitude - self.latitude) ** 2
        return sqrt(x2 + y2)


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_bars = json.load(f);
        bars = []
        for raw_bar in raw_bars:
            bars.append(Bar(raw_bar))
        return bars


def get_biggest_bar(bars):
    biggest_bar = bars[0]
    for bar in bars:
        if bar.seat_count > biggest_bar.seat_count:
            biggest_bar = bar
    return biggest_bar


def get_smallest_bar(bars):
    smallest_bar = bars[0]
    for bar in bars:
        if bar.seat_count < smallest_bar.seat_count:
            smallest_bar = bar
    return smallest_bar


def get_closest_bar(bars, longitude, latitude):
    closest_bar = bars[0]
    closest_distance = closest_bar.distance_to(longitude, latitude)
    for bar in bars:
        current_distance = bar.distance_to(longitude, latitude) 
        if current_distance < closest_distance:
            closest_bar = bar
            closest_distance = current_distance
    return closest_bar


def print_usage():
    print('TODO: write usage statement', file=sys.stderr)


def print_biggest_bar(data_file):
    print(get_biggest_bar(load_data(data_file)).name)


def print_smallest_bar(data_file):
    print(get_smallest_bar(load_data(data_file)).name)


def print_closest_bar(data_file):
    longitude, latitude = [float(s) for s in input().split()]
    bar = get_closest_bar(load_data(data_file), longitude, latitude)
    print(b.name, b.longitude, b.latitude)


options = {'biggest': print_biggest_bar, 'smallest': print_smallest_bar,
           'closest': print_closest_bar}

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('The wrong number of arguments is supplied.', file=sys.stderr)
        print_usage()
    else:
        for opt in options:
            if opt == sys.argv[1]:
                options[opt](sys.argv[2])
                break;
        else:
            print('Unknown option.', file=sys.stderr)
            print_usage()
