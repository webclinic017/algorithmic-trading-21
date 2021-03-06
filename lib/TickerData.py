from backtrader.feeds import PandasData

class TickerData(PandasData):
    OHLCV = ['datetime','open', 'high', 'low', 'close', 'volume']
    cols = OHLCV + ['predicted', 'sentiment_neg','sentiment_neu','sentiment_pos', 'sentiment_compound']

    lines = tuple(cols)

    params = {c: -1 for c in cols}
    # params.update({'datetime': None})
    params = tuple(params.items())
