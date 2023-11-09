#!/usr/bin/env python3

import argparse
import csv
import datetime
from dataclasses import dataclass
import sys


def main():
    parser = argparse.ArgumentParser(
        prog='convert_forecast',
        description='Converts csv files from EMI web site internal format to app format',
    )
    parser.add_argument('forecast', help='Read forecast from this file.')
    parser.add_argument('-t', '--forecast-time', required=True,
                        help='First day of forecast. Use a format like 2023-10-29')
    parser.add_argument('-o', '--output-file', required=False,
                        help='Write results to this file. If not given, use stdout')

    args = parser.parse_args()

    forecast_time = datetime.datetime.strptime(args.forecast_time, '%Y-%m-%d')

    cities = CityLookup('cities.csv')

    output_file = sys.stdout
    if args.output_file:
        output_file = open(args.output_file, 'w', newline='')

    writer = csv.DictWriter(
        output_file,
        ['city', 'temprature_min', 'temprature_max',
            'weather_condition', 'early_warning', 'forecast_date']
    )
    writer.writeheader()

    with output_file:
        with open(args.forecast, newline='') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                try:
                    city = cities.id(row['Weather Location'])
                except KeyError as e:
                    print('unkonwn city:', e)
                    continue

                for i in range(1, 4):
                    t = forecast_time + datetime.timedelta(days=i-1)
                    try:
                        weather_condition = weather_conditions[row[f'Wthr{i}'].upper(
                        )]
                    except KeyError:
                        print('unrecognized weather condition:',
                              row[f'Wthr{i}'])
                        continue
                    output = {
                        # 'id': None,
                        'city': city,
                        'temprature_min': float(row[f'Min {i}']),
                        'temprature_max': float(row[f'Max {i}']),
                        'weather_condition': weather_condition,
                        'early_warning': early_warning(row[f'Wthr{i}'].upper()),
                        'forecast_date': t.strftime('%Y-%m-%d 00:00:00'),
                    }
                    writer.writerow(output)


def early_warning(weather_condition: str) -> str:
    try:
        return warnings[weather_condition]
    except KeyError:
        pass
    return ''


class CityLookup:
    def __init__(self, city_file: str):
        cities = {}
        with open(city_file, newline='') as f:
            for city in csv.reader(f, delimiter=','):
                cities[city[1].lower()] = int(city[0])
        self.cities = cities

    def id(self, name: str) -> int:
        return self.cities[name.lower().strip()]


weather_conditions = {
    'S': 1,  # Sunny
    'C': 2,  # Cloudy
    'PC': 4,  # Partial Cloudy
    'R': 5,  # Rainy
    # 6, # Stormy
    # 7, # Rain with Sun
    # 8, # Heavy Rain
    # 9, # Rain Showers
    'F': 14,  # Fog
    'LR': 16,  # Light Rain
    'MS': 1,  # Mostly Sunny
}

warnings = {
    'S': 'Wear breathable cloth and drink plenty of water',
    'C': 'Bring jacket',
    'PC': 'Wear light jacket',
    'R': 'Wear rainy coat and use umbrella',
    'F': '',
    'LR': 'Bring umbrella',
    'MS': 'Wear light cotton cloth'
}

if __name__ == '__main__':
    main()
