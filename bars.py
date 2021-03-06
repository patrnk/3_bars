from json import load
from math import sqrt
from argparse import ArgumentParser
from os.path import exists
from sys import exit


def distance_to(bar, longitude, latitude):
    x2 = (longitude - bar['geoData']['coordinates'][0]) ** 2
    y2 = (latitude - bar['geoData']['coordinates'][1]) ** 2
    return sqrt(x2 + y2)


def get_closest_bar(bars, longitude, latitude):
    distance = lambda bar: distance_to(bar, longitude, latitude)
    return min(bars, key=distance)


def get_biggest_bar(bars):
    return max(bars, key=lambda bar: int(bar['SeatsCount']))


def get_smallest_bar(bars):
    return min(bars, key=lambda bar: int(bar['SeatsCount']))


def load_data(filepath):
    with open(filepath, encoding='cp1251') as f:
        return load(f)


def print_bar(bar):
    print('Название: {0}'.format(bar['Name']))
    print('Адрес: {0}, {1}'.format(bar['District'], bar['Address']))
    print('Телефон: {0}'.format(bar['PublicPhone'][0]['PublicPhone']))


def get_argument_parser():
    parser = ArgumentParser()
    parser.add_argument('what_to_look_for', type=str, 
            help='говорит скрипту, что нужно найти: '\
                 'biggest, smallest или closest')
    parser.add_argument('json_filepath', help='файл с данными о барах')
    return parser


if __name__ == '__main__':
    options = {
        'biggest': get_biggest_bar,
        'smallest': get_smallest_bar,
        'closest': get_closest_bar
    }
    args = get_argument_parser().parse_args()

    option = options.get(args.what_to_look_for)
    if not option:
        exit('Неизвестный аргумент {0}'.format(args.what_to_look_for))
    if not exists(args.json_filepath):
        exit('Файл с барами не найден.')

    bars = load_data(args.json_filepath)

    kwargs = {'bars': bars}
    if args.what_to_look_for == 'closest':
        message = 'Введите долготу и ширину: '
        longitude, latitude = [float(s) for s in input(message).split()]
        kwargs['longitude'], kwargs['latitude'] = longitude, latitude 

    bar = option(**kwargs)
    print_bar(bar)
