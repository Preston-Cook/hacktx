import requests
import os
import sys

OW_API_KEY = os.environ.get('OW_API_KEY')

if not OW_API_KEY:
    print('ERROR: Open AI API key not set')
    sys.exit(1)


def retrieve_weather(prompt):

    try:
        res = requests.get('http://ipinfo.io')
        res.raise_for_status()

    except requests.exceptions.HTTPError as e:
        print(e)
        sys.exit(1)

    json_res = res.json()

    lat, lng = json_res['loc'].split(',')

    if json_res['country'] == 'US':
        units = 'imperial'
    else:
        units = 'metric'

    try:
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={OW_API_KEY}&units={units}')
        res.raise_for_status()

    except requests.exceptions.HTTPError as e:
        return "I'm currently unable to gather weather information on your location"

    json_res = res.json()

    location = json_res['name']
    temperature = round(json_res['main']['temp'])
    description = json_res['weather'][0]['description']
    high = round(json_res['main']['temp_max'])
    low = round(json_res['main']['temp_min'])

    degrees = 'Celsius' if units == 'metric' else 'Fahrenheit'

    return f'In {location}, it is currently {temperature} degrees {degrees}. Today you can expect {description} with a high of {high} and a low of {low}.'