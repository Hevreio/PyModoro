import requests
from const_value import API, KEY, UNIT, LANGUAGE, LOCATION


def fetchWeather(location):
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT
    }, timeout=1)
    return result.json()


if __name__ == '__main__':
    dct = fetchWeather(LOCATION)
    print(dct['results'][0]['location'])

