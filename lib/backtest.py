import backtrader as bt
from alpaca_trade_api.rest import TimeFrame
from lib.api_client import rest_api
from lib.prediction import classification
import pandas as pd
from lib.TickerData import TickerData
from datetime import datetime, timedelta
import numpy as np

def pick_best(df, strategy):
    print(f'strategy: {strategy}')
    print(type(df))
    predictions = df[strategy]
    predictions = pd.DataFrame(predictions)
    predictions.rename(columns = {strategy: 'predicted'}, inplace=True)
    return predictions

def pick_best_strategy(ticker, start, end, cash=10000, timeframe=TimeFrame.Day):
    train_data = rest_api.get_bars(ticker, timeframe, start, end, adjustment='all').df
    print(train_data)
    predictions, strategies = classification.predict(train_data['close'])
    return predictions[strategies].cumsum().apply(np.exp)[strategies].max().idxmax()

def backtest(strategy, tickers, start, end, cash=10000, timeframe=TimeFrame.Day):
    sandbox = bt.Cerebro(stdstats=True)
    sandbox.broker.setcash(cash)
    sandbox.addstrategy(strategy)
    sandbox.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')

    if type(tickers) == str:
        tickers = [tickers]
    if type(tickers) == list:
        for ticker in tickers:
            alpaca_data = rest_api.get_bars(ticker, timeframe, start, end, adjustment='all').df
            
            train_start = datetime.strptime(start,'%Y-%m-%d') - timedelta(days = 1200)
            train_end = start
            print(train_start.date())
            best_strategy = pick_best_strategy(ticker,train_start.date(),train_end)


            predictions, _ = classification.predict(alpaca_data['close'])
            print(best_strategy)
            predictions = pick_best(predictions, best_strategy)
            prices = predictions.join(alpaca_data, how='right').dropna()

            data = TickerData(dataname=prices, name=ticker)

            sandbox.adddata(data)

    initial_cash = sandbox.broker.getvalue()
    print(f'Starting value: {initial_cash}')
    results = sandbox.run()
    
    final_cash = sandbox.broker.getvalue()
    print(f'Final value: ${final_cash}')
    return_percentage = (final_cash / initial_cash - 1) * 100
    print(f'Return: {return_percentage}%')

    strat = results[0]
    print('Sharpe Ratio:', strat.analyzers.mysharpe.get_analysis()['sharperatio'])
    sandbox.plot(iplot=False)