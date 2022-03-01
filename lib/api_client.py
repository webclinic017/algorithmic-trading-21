from alpaca_trade_api.rest import REST
from dotenv import load_dotenv

import os

load_dotenv()

api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')
rest_api = REST(api_key, secret_key, 'https://paper-api.alpaca.markets')
