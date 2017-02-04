import sys
import json
from math import sqrt


def distance_to(bar, longitude, latitude):
    x2 = (longitude - bar['geoData']['coordinates'][0]) ** 2
    y2 = (latitude - bar['geoData']['coordinates'][1]) ** 2
    return sqrt(x2 + y2)


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_biggest_bar(kwargs):
    return max(kwargs['bars'], key=lambda bar: int(bar['SeatsCount']))


def get_smallest_bar(kwargs):
    return min(kwargs['bars'], key=lambda bar: int(bar['SeatsCount']))


def get_closest_bar(kwargs):
    longitude, latitude = kwargs['longitude'], kwargs['latitude']
    distance = lambda bar: distance_to(bar, longitude, latitude)
    return min(kwargs['bars'], key=distance)


def print_usage_and_exit(kwargs):
    name = kwargs['script_name']
    print('usage: ' + name + ' mode file_name', file=sys.stderr)
    print('     mode принимает следующие значения:', file=sys.stderr)
    print('     - biggest (показать самый большой бар)', file=sys.stderr)
    print('     - smallest (показать самый маленький бар)', file=sys.stderr)
    print('     - closest (показать ближайший бар)', file=sys.stderr)
    print('     file_name - это имя JSON файла ' + \
          'с данными о барах', file=sys.stderr)
    sys.exit(1)


def print_bar(bar):
    print('Название: ' + bar['Name'])
    print('Адрес: ' + bar['District'] + ', ' + bar['Address'])
    print('Телефон: ' + bar['PublicPhone'][0]['PublicPhone'])


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Неверно количество введенных аргументов.', file=sys.stderr)
        print_usage_and_exit(sys.argv[0])
    try:
        bars = load_data(sys.argv[2])
    except FileNotFoundError:
        raise SystemExit('Файл не найден.')

    options = {'biggest': get_biggest_bar, 'smallest': get_smallest_bar,
               'closest': get_closest_bar}
    kwargs = {'bars': bars, 'script_name': sys.argv[2]}
    if sys.argv[1] == 'closest':
        message = 'Введите долготу и ширину: '
        longitude, latitude = [float(s) for s in input(message).split()]
        kwargs['longitude'], kwargs['latitude'] = longitude, latitude 

    bar = options.get(sys.argv[1], print_usage_and_exit)(kwargs)
    print_bar(bar)
