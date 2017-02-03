import sys
import json
from math import sqrt


class Bar:

    def __init__(self, json_data):
        self.seat_count = json_data['SeatsCount']
        self.longitude = float(json_data['geoData']['coordinates'][0])
        self.latitude = float(json_data['geoData']['coordinates'][1])
        self.name = json_data['Name']
        self.address = json_data['District'] + ', ' + json_data['Address']
        self.telephone = json_data['PublicPhone'][0]['PublicPhone']

    def distance_to(self, longitude, latitude):
        x2 = (longitude - self.longitude) ** 2
        y2 = (latitude - self.latitude) ** 2
        return sqrt(x2 + y2)


def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_bars = json.load(f);
            bars = []
            for raw_bar in raw_bars:
                bars.append(Bar(raw_bar))
            return bars
    except FileNotFoundError:
        raise SystemExit('File is not found.')


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


def print_usage(name):
    print('usage: ' + name + ' mode file_name', file=sys.stderr)
    print('       mode is either:', file=sys.stderr)
    print('       - biggest (outputs the biggest bar)', file=sys.stderr)
    print('       - smallest (outputs the smallest bar)', file=sys.stderr)
    print('       - closest (outputs the closest bar)', file=sys.stderr)
    print('       file_name is the name of the .json file', file=sys.stderr)
    print('         with data about the bars', file=sys.stderr)


def print_bar(bar):
    print('Название: ' + bar.name)
    print('Адрес: ' + bar.address)
    print('Телефон: ' + bar.telephone)


def print_biggest_bar(data_file):
    biggest_bar = get_biggest_bar(load_data(data_file)).name 
    print_bar(biggest_bar)


def print_smallest_bar(data_file):
    smallest_bar = get_smallest_bar(load_data(data_file)).name
    print_bar(smallest_bar)


def print_closest_bar(data_file):
    bars = load_data(data_file)
    message = 'Please enter your longitude and latitude: '
    longitude, latitude = [float(s) for s in input(message).split()]
    bar = get_closest_bar(bars, longitude, latitude)
    print_bar(bar)


options = {'biggest': print_biggest_bar, 'smallest': print_smallest_bar,
           'closest': print_closest_bar}

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('The wrong number of arguments is supplied.', file=sys.stderr)
        print_usage(sys.argv[0])
    else:
        for opt in options:
            if opt == sys.argv[1]:
                options[opt](sys.argv[2])
                break;
        else:
            print('Unknown option.', file=sys.stderr)
            print_usage(sys.argv[0])
