import backtrader as bt
from alpaca_trade_api.rest import TimeFrame
from api_client import rest_api

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
            data = bt.feeds.PandasData(dataname=alpaca_data, name=ticker)
            sandbox.adddata(data)

    initial_cash = sandbox.broker.getvalue()
    print(f'Starting value: {initial_cash}')
    results = sandbox.run()
    
    final_cash = sandbox.broker.getvalue()
    print(f'Final value: ${final_cash}')
    return_percentage = (final_cash / initial_cash - 1) * 100
    print(f'Return: ${return_percentage}%')

    strat = results[0]
    print('Sharpe Ratio:', strat.analyzers.mysharpe.get_analysis()['sharperatio'])
    sandbox.plot(iplot=False)