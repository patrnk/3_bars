import json
from math import sqrt


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


def distance_to(bar, longitude, latitude):
    lon = float(bar['Longitude_WGS84'])
    lat = float(bar['Latitude_WGS84'])
    return sqrt((lon - longitude) ** 2 + (lat - latitude) ** 2)


def get_closest_bar(data, longitude, latitude):
    closest_bar = data[0]
    closest_distance = distance_to(data[0], longitude, latitude)
    for bar in data:
        current_distance = distance_to(bar, longitude, latitude) 
        if current_distance < closest_distance:
            closest_bar = bar
            closest_distance = current_distance
    return closest_bar


if __name__ == '__main__':
    longitude, latitude = [float(s) for s in input().split()]
    b = get_closest_bar(load_data('data.json'), longitude, latitude)
    print(b['Name'], b['Longitude_WGS84'], b['Latitude_WGS84'])
