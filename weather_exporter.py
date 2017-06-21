#!/usr/bin/env python3

from prometheus_client import start_http_server, Gauge
import pyowm
from time import sleep
from daemonize import Daemonize

pid = "/var/run/weather_exporter.pid"
owm_key = ''
def app():
    owm = pyowm.OWM(owm_key)

    temperature = Gauge('temperature_vancouver', 'Temperature, Celsius')
    wind_speed = Gauge('wind_speed', 'Wind speed, m/s')
    wind_direction = Gauge('wind_direction', 'Wind direction, deg')
    humidity = Gauge('humidity', 'Humidity, % ')
    pressure = Gauge('pressure', 'Pressure, % hPa')
    clouds = Gauge('clouds', 'Cloudiness , %')

    while True:
        observation = owm.weather_at_place('Vancouver,ca')
        w = observation.get_weather()
        temperature.set(w.get_temperature('celsius')['temp'])
        wind_speed.set(w.get_wind()['speed'])
        wind_direction.set(w.get_wind()['deg'])
        humidity.set(w.get_humidity())
        pressure.set(w.get_pressure()['press'])
        clouds.set(w.get_clouds())
        sleep(10)

def main()
    start_http_server(9000)
    app()

daemon = Daemonize(app="weather_exporter", pid=pid, action=main)
daemon.start()
