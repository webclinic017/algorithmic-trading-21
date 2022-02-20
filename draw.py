import plotly.graph_objects as go
import plotly.express as px

def plot_candlestick(bars):
    candlestick = go.Candlestick(x=bars.index,
        open=bars['open'],
        high=bars['high'],
        low=bars['low'],
        close=bars['close'])
    candlestick_fig = go.Figure(data=[candlestick])

    sma = bars['close'].rolling(15).mean().dropna()

    sma_fig = px.line(x=sma.index, y=sma)

    fig = go.Figure(data=candlestick_fig.data + sma_fig.data)
    
    fig.show()