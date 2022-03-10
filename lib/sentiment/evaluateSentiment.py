from lib.api_client import rest_api
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from functools import reduce
from datetime import datetime, timedelta
import logging

logging.basicConfig(filename=".logs/sentiment.log", level=logging.INFO, filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


nltk.downloader.download('vader_lexicon') 
new_words = {
    'citron': -4.0,  
    'hidenburg': -4.0,        
    'moon': 4.0,
    'highs': 2.0,
    'mooning': 4.0,
    'long': 2.0,
    'short': -2.0,
    'call': 4.0,
    'calls': 4.0,    
    'put': -4.0,
    'puts': -4.0,    
    'break': 2.0,
    'tendie': 2.0,
     'tendies': 2.0,
     'town': 2.0,     
     'overvalued': -3.0,
     'undervalued': 3.0,
     'buy': 4.0,
     'sell': -4.0,
     'gone': -1.0,
     'gtfo': -1.7,
     'paper': -1.7,
     'bullish': 3.7,
     'bearish': -3.7,
     'bagholder': -1.7,
     'stonk': 1.9,
     'green': 1.9,
     'money': 1.2,
     'print': 2.2,
     'rocket': 2.2,
     'bull': 2.9,
     'bear': -2.9,
     'pumping': -1.0,
     'sus': -3.0,
     'offering': -2.3,
     'rip': -4.0,
     'downgrade': -3.0,
     'upgrade': 3.0,     
     'maintain': 1.0,          
     'pump': 1.9,
     'hot': 1.5,
     'drop': -2.5,
     'rebound': 1.5,  
     'crack': 2.5,}

def sentiment_per_day(ticker, days):
    return list(map(lambda single_date: evaluate_sentiment(ticker, single_date, single_date), days))

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def evaluate_sentiment(ticker, start,end):
    news = rest_api.get_cached_news(ticker, start, end)
    if len(news) == 0:
        return {
            'date': start,
            'neg': 0,
            'neu': 1,
            'pos': 0,
            'compound': 0}
    vader = SentimentIntensityAnalyzer()
    vader.lexicon.update(new_words)
    
    words_scores = [vader.polarity_scores(word) for sentence in news for word in sentence['headline'].split()]

    scores_keys = ['neg','neu','pos','compound']
    final_score = {'date': start}
    for key in scores_keys:
        final_score[key] = reduce(lambda acc,item:acc+item[key], words_scores, 0) / len(words_scores)


    logger.info(final_score)
    return final_score

