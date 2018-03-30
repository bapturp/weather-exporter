import sys, time, argparse

from prometheus_client import start_http_server, Gauge
import pyowm

def app(city, key):
    owm = pyowm.OWM(key)

    temperature = Gauge('temperature', 'Temperature, Celsius', ['city'])
    wind_speed = Gauge('wind_speed', 'Wind speed, m/s', ['city'])
    wind_direction = Gauge('wind_direction', 'Wind direction, deg', ['city'])
    humidity = Gauge('humidity', 'Humidity, % ', ['city'])
    pressure = Gauge('pressure', 'Pressure, % hPa', ['city'])
    clouds = Gauge('clouds', 'Cloudiness , %', ['city'])

    while True:
        observation = owm.weather_at_place(city)
        w = observation.get_weather()

        temperature.labels(city).set(w.get_temperature('celsius')['temp'])
        wind_direction.labels(city).set(w.get_wind()['deg'])
        humidity.labels(city).set(w.get_humidity())
        pressure.labels(city).set(w.get_pressure()['press'])
        clouds.labels(city).set(w.get_clouds())
        time.sleep(10)

def parse_args():
    parser = argparse.ArgumentParser(description='weather exporter args port')

    parser.add_argument(
        '-p', '--port',
        metavar='port',
        required=False,
        type=int,
        help='Listen to this port',
        default='9000'
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
        start_http_server(args.port)
        app(city=args.city, key=args.key)
    except KeyboardInterrupt:
        sys.exit('Interrupted')

if __name__ == '__main__':
    main()

