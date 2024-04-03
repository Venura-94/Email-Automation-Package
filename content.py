import csv
import random
import requests
import json
import datetime
import urllib.request as request


def get_random_quote(quotes_file='quotes.csv'):
    try:  # load motivational quotes from csv file
        with open(quotes_file) as csvfile:
            quotes = [{'author': line[0], 'quote': line[1]} for line in csv.reader(csvfile, delimiter='|')]

    except Exception as e:  # handle exception
        quotes = [{'author': 'Eric Idle', 'quote': 'Always Look on the Bright Side of Life.'}]
    return random.choice(quotes)


def get_weather_forecast(coords={'lat': 6.8479, 'lon': 80.0484}):
    try:  # retrieve forecast for specified coordinates
        api_key = ""
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={coords["lat"]}&lon={coords["lon"]}&appid={api_key}&units=metric'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()

            forecast = {'city': data['city']['name'],  # city name
                        'country': data['city']['country'],  # country name
                        'periods': list()}  # list to hold forecast data for future periods

            for period in data['list'][0:9]:  # populate list with next 9 forecast periods
                forecast['periods'].append({'timestamp': datetime.datetime.fromtimestamp(period['dt']),
                                            'temp': round(period['main']['temp']),
                                            'description': period['weather'][0]['description'].title(),
                                            'icon': f'http://openweathermap.org/img/wn/{period["weather"][0]["icon"]}.png'})
            return forecast
        else:
            print(f"Error: {response.status_code}")
            return None

    except Exception as e:
        print(e)
        return None

def get_wikipedia_article():
    try: # retrieve random Wikipedia article
        data = json.load(request.urlopen('https://en.wikipedia.org/api/rest_v1/page/random/summary'))
        return {'title': data['title'],
                'extract': data['extract'],
                'url': data['content_urls']['desktop']['page']}

    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    ##### test get_random_quote() #####
    print('\nTesting quote generation...')

    quote = get_random_quote()
    print(f' - Random quote is "{quote["quote"]}" - {quote["author"]}')

    quote = get_random_quote(quotes_file=None)
    print(f' - Default quote is "{quote["quote"]}" - {quote["author"]}')

    ##### test get_weather_forecast() #####
    print('\nTesting weather forecast retrieval...')

    forecast = get_weather_forecast()  # get forecast for default location
    if forecast:
        print(f'\nWeather forecast for {forecast["city"]}, {forecast["country"]} is...')
        for period in forecast['periods']:
            print(f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}')

    austin = {'lat': 6.8479, 'lon': 80.0484}  # coordinates for Texas State Capitol
    forecast = get_weather_forecast(coords=austin)  # get Austin, TX forecast
    if forecast:
        print(f'\nWeather forecast for {forecast["city"]}, {forecast["country"]} is...')
        for period in forecast['periods']:
            print(f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}')

    invalid = {'lat': 1234.5678, 'lon': 1234.5678}  # invalid coordinates
    forecast = get_weather_forecast(coords=invalid)  # get forecast for invalid location
    if forecast is None:
        print('Weather forecast for invalid coordinates returned None')

        ##### test get_wikipedia_article() #####
    print('\nTesting random Wikipedia article retrieval...')

    article = get_wikipedia_article()
    if article:
        print(f'\n{article["title"]}\n<{article["url"]}>\n{article["extract"]}')
