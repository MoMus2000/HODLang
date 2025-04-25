from abc import ABC, abstractmethod

class BackTest(ABC):
    def __init__(self, executor):
        self.executor = executor

    @abstractmethod
    def run_backtest(self):
        pass

    @abstractmethod
    def rebalance(self, asset_values, weights):
        pass

    @abstractmethod
    def set_portfolio(self, executor):
        pass

