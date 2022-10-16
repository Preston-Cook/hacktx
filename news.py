import requests
import os
import sys
from newsapi import NewsApiClient

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

if not NEWS_API_KEY:
    print('ERROR: Open News API key not set')
    sys.exit(1)

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def retrieve_news(prompt):

    try:
        res = requests.get('http://ipinfo.io')
        res.raise_for_status()
    
    except requests.exceptions.HTTPError as e:
        print(e)
        return "I'm currently unable to retrieve information on news"
    
    json_res = res.json()

    country = json_res['country']

    if not country:
        country = 'us'
    else:
        country = country.lower()

    hl1, hl2, hl3 = [newsapi.get_top_headlines(country=country)['articles'][i]['title'] for i in range(3)]
    
    return f'In the news: {hl1}, {hl2}, and {hl3}.'