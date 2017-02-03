import json
from math import sqrt


class Bar:

    def __init__(self, json_data):
        self.seat_count = json_data['SeatsCount']
        self.longitude = float(json_data['Longitude_WGS84'])
        self.latitude = float(json_data['Latitude_WGS84'])
        self.name = json_data['Name']

    def distance_to(self, another_bar):
        x2 = (another_bar.longitude - self.longitude) ** 2
        y2 = (another_bar.latitude - self.latitude) ** 2
        return sqrt(x2 + y2)


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_bars = json.load(f);
        bars = []
        for raw_bar in raw_bars:
            bars.append(Bar(raw_bar))
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
    #longitude, latitude = [float(s) for s in input().split()]
    #b = get_closest_bar(load_data('data.json'), longitude, latitude)
    #print(b['Name'], b['Longitude_WGS84'], b['Latitude_WGS84'])
    
    for bar in load_data('data.json'):
        print(bar.name)
    #print(get_biggest_bar(load_data('data.json')))
