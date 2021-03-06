from alpaca_trade_api.rest import REST, TimeFrame
from lib.draw import plot_candlestick
from lib.backtest import backtest
from lib.strategy import SimpleStrategy
from lib.api_client import rest_api
from lib.choose_company import get_best_company

def run():
    print('algorithm is running')
    data = prepare_data()
    company_ticker = 'AAPL'#get_best_company()
    print(company_ticker)
    # plot_candlestick(data)
    backtest(SimpleStrategy, company_ticker, '2021-06-10', '2022-01-01')
  

def prepare_data():
    spy_bars = rest_api.get_bars('SPY', TimeFrame.Day, '2021-01-01', '2021-03-30').df
    return spy_bars
