import yfinance as yf

class BackTest:
    def __init__(self, executor):
        self.executor = executor
        self.tickers  = []

    def run_backtest(self):
        print("** Loading Data **")
        for ticker in self.executor.portfolio["tickers"]:
            self.tickers.append(yf.Ticker(ticker))

        for yf_ticker in self.tickers:
            print(yf_ticker.history(period="10d"))
