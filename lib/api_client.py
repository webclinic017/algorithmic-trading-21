from alpaca_trade_api.rest import REST, NewsListV2
from dotenv import load_dotenv
import time
import os
from os.path import exists
import json
import pickle
from json import JSONEncoder
import requests
import pandas as pd

load_dotenv()

api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')
fmp_key = os.getenv('FMP_API_KEY')



def mapNewsListV2(news):
    return {
        'author': news.author,
        'created_at': str(news.created_at),
        'headline': news.headline,
        'id': news.id,
        'images': news.images,
        'source': news.source,
        'summary': news.summary,
        'symbols': news.symbols,
        'updated_at': str(news.updated_at),
        'url': news.url
    }

class Cached_rest(REST):

    def get_cached_news(self,ticker, start, end, limit=100):
        news = []
        cache_file_dir = os.path.join('.cache/', ticker + start)
        if exists(cache_file_dir):
            with open(cache_file_dir, "r") as fp:
                news = json.load(fp)
        else:
            raw_news = self.get_news(ticker, start, end, limit=100)
            news = list(map(mapNewsListV2, raw_news))
            with open(cache_file_dir, "w") as fp:
                json.dump(news, fp)      
        return news

    def get_key_executives(self,ticker):
        html_text = None
        cache_file_dir = os.path.join('.cache/', ticker + '-key-executives')
        if exists(cache_file_dir):
            with open(cache_file_dir, "r") as fp:
                html_text = json.load(fp)
        else:
            url = 'https://finance.yahoo.com/quote/'+ ticker + '/profile'
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
            html = requests.get(url, headers=headers, timeout=5)
            html_text = html.text
            with open(cache_file_dir, "w") as fp:
                json.dump(str(html_text), fp) 

        try:
            return pd.read_html(html_text)[0]
        except:
            return pd.DataFrame()

    def get_tickers(self):
        url = 'https://www.slickcharts.com/nasdaq100'
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        html = requests.get(url, headers=headers, timeout=5)
        tickers = pd.read_html(html.text)[0]['Symbol'].tolist()
        return tickers

rest_api = Cached_rest(api_key, secret_key, 'https://paper-api.alpaca.markets')