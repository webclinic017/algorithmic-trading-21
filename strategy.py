import backtrader as bt


class SimpleStrategy(bt.Strategy):
    params = dict(pfast=24,pslow=25)

    def __init__(self):
        sma_fast = bt.ind.SMA(period=self.p.pfast)
        sma_slow = bt.ind.SMA(period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(sma_fast, sma_slow)
        
        sma_slow.plotinfo.subplot = False
        sma_slow.plotinfo.subplot = False
        self.crossover.plotinfo.subplot = False
    
    def next(self):
        if not self.position and self.crossover > 0:
            self.buy()
        elif self.position and self.crossover < 0:
            self.close()