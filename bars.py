from json import load
from math import sqrt
from argparse import ArgumentParser
from sys import exit


def distance_to(bar, longitude, latitude):
    x2 = (longitude - bar['geoData']['coordinates'][0]) ** 2
    y2 = (latitude - bar['geoData']['coordinates'][1]) ** 2
    return sqrt(x2 + y2)


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return load(f)


def get_biggest_bar(kwargs):
    return max(kwargs['bars'], key=lambda bar: int(bar['SeatsCount']))


def get_smallest_bar(kwargs):
    return min(kwargs['bars'], key=lambda bar: int(bar['SeatsCount']))


def get_closest_bar(kwargs):
    longitude, latitude = kwargs['longitude'], kwargs['latitude']
    distance = lambda bar: distance_to(bar, longitude, latitude)
    return min(kwargs['bars'], key=distance)


def print_bar(bar):
    print('Название: ' + bar['Name'])
    print('Адрес: ' + bar['District'] + ', ' + bar['Address'])
    print('Телефон: ' + bar['PublicPhone'][0]['PublicPhone'])


def get_cli_args():
    parser = ArgumentParser()
    parser.add_argument('what_to_look_for', type=str, 
            help='говорит скрипту, что нужно найти: ' +\
                 'biggest, smallest или closest')
    parser.add_argument('json_file', help='файл с данными о барах')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_cli_args()
    try:
        bars = load_data(args.json_file)
    except FileNotFoundError:
        raise SystemExit('Файл не найден.')

    options = {'biggest': get_biggest_bar, 'smallest': get_smallest_bar,
               'closest': get_closest_bar}
    kwargs = {'bars': bars}

    if args.what_to_look_for == 'closest':
        message = 'Введите долготу и ширину: '
        longitude, latitude = [float(s) for s in input(message).split()]
        kwargs['longitude'], kwargs['latitude'] = longitude, latitude 

    bar = options.get(args.what_to_look_for, None)(kwargs)
    if bar == None:
        exit('Uknown argument %s' % what_to_look_for)
    print_bar(bar)
