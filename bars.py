import sys
import json
from math import sqrt


def distance_to(bar, longitude, latitude):
    x2 = (longitude - bar['geoData']['coordinates'][0]) ** 2
    y2 = (latitude - bar['geoData']['coordinates'][1]) ** 2
    return sqrt(x2 + y2)


def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit('Файл не найден.')


def get_biggest_bar(bars):
    return max(bars, key=lambda bar: int(bar['SeatsCount']))


def get_smallest_bar(bars):
    return min(bars, key=lambda bar: int(bar['SeatsCount']))


def get_closest_bar(bars, longitude, latitude):
    return min(bars, key=lambda bar: distance_to(bar, longitude, latitude))


def print_usage(name):
    print('usage: ' + name + ' mode file_name', file=sys.stderr)
    print('     mode принимает следующие значения:', file=sys.stderr)
    print('     - biggest (показать самый большой бар)', file=sys.stderr)
    print('     - smallest (показать самый маленький бар)', file=sys.stderr)
    print('     - closest (показать ближайший бар)', file=sys.stderr)
    print('     file_name - это имя JSON файла', file=sys.stderr)
    print('                 с данными о барах', file=sys.stderr)


def print_bar(bar):
    print('Название: ' + bar['Name'])
    print('Адрес: ' + bar['District'] + ', ' + bar['Address'])
    print('Телефон: ' + bar['PublicPhone'][0]['PublicPhone'])


def print_biggest_bar(data_file):
    biggest_bar = get_biggest_bar(load_data(data_file))
    print_bar(biggest_bar)


def print_smallest_bar(data_file):
    smallest_bar = get_smallest_bar(load_data(data_file))
    print_bar(smallest_bar)


def print_closest_bar(data_file):
    bars = load_data(data_file)
    message = 'Введите долготу и ширину: '
    longitude, latitude = [float(s) for s in input(message).split()]
    bar = get_closest_bar(bars, longitude, latitude)
    print_bar(bar)


options = {'biggest': print_biggest_bar, 'smallest': print_smallest_bar,
           'closest': print_closest_bar}

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Неверно количество введенных аргументов.', file=sys.stderr)
        print_usage(sys.argv[0])
    else:
        for opt in options:
            if opt == sys.argv[1]:
                options[opt](sys.argv[2])
                break;
        else:
            print('Неизвестный аргумент.', file=sys.stderr)
            print_usage(sys.argv[0])
