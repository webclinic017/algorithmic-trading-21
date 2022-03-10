import backtrader as bt


class SimpleStrategy(bt.Strategy):

    def __init__(self):
        # sma_fast = bt.ind.SMA(period=2)
        # sma_slow = bt.ind.SMA(period=5)
        # self.crossover = bt.ind.CrossOver(sma_fast, sma_slow)
        # self.crossover.plotinfo.subplot = True
        
        self.data_predicted = self.datas[0].predicted
        self.data_open = self.datas[0].open
        self.data_close = self.datas[0].close
        self.data_sentiment_pos = self.datas[0].sentiment_pos
        self.data_sentiment_neg = self.datas[0].sentiment_neg

        self.order = None
        self.price = None
        self.comm = None

    def next(self):
        positive = self.data_sentiment_pos > self.data_sentiment_neg
        negative = self.data_sentiment_pos < self.data_sentiment_neg

        if not self.position and self.data_predicted > 0 and positive:
            
            size = int(self.broker.getcash() / self.datas[0].open)
            self.buy(size=size)
        elif self.position and self.data_predicted < 0 and negative:
            
            self.sell(size=self.position.size)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
          
                self.price = order.executed.price
                self.comm = order.executed.comm

        self.order = None