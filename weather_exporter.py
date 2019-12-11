#!/usr/bin/env python
import sys
import time
import argparse

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, GaugeMetricFamily

import pyowm


class WeatherCollector:
    def __init__(self, city, key):
        self.city = city
        self.key = key
        self.owm = pyowm.OWM(self.key)
    
    def get_weather(self):
        observation = self.owm.weather_at_place(self.city)
        return observation.get_weather()

    def collect(self):
        weather = self.get_weather()
        
        temperature = GaugeMetricFamily('temperature', 'Temperature, Celsius', labels=['city'])
        temperature.add_metric([self.city], weather.get_temperature('celsius')['temp'])
        
        humidity = GaugeMetricFamily('humidity', 'Humidity, %', labels=['city'])
        humidity.add_metric([self.city], weather.get_humidity())

        wind_direction = GaugeMetricFamily('wind_direction', 'Wind direction, deg', labels=['city'])
        wind_direction.add_metric([self.city], weather.get_wind()['deg'])

        pressure = GaugeMetricFamily('pressure', 'Pressure, % hPa', labels=['city'])
        pressure.add_metric([self.city], weather.get_pressure()['press'])

        clouds = GaugeMetricFamily('clouds', 'Cloudiness, %', labels=['city'])
        clouds.add_metric([self.city], weather.get_clouds())

        for metric in (temperature, humidity, wind_direction, pressure, clouds):
            yield metric


def parse_args():
    parser = argparse.ArgumentParser(description='weather exporter args port, city and key')

    parser.add_argument(
        '-p', '--port',
        metavar='port',
        required=False,
        type=int,
        help='Listen to this port',
        default='9123'
    )

    parser.add_argument(
        '-c', '--city',
        metavar='city',
        required=True,
        type=str,
        help='City and country formatted city,co',
    )

    parser.add_argument(
        '-k', '--key',
        metavar='key',
        required=True,
        type=str,
        help='Open Weather Map API key'
    )

    return parser.parse_args()


def main():
    try:
        args = parse_args()
        REGISTRY.register(WeatherCollector(args.city, args.key))
        start_http_server(args.port)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit('Interrupted')


if __name__ == '__main__':
    main()
