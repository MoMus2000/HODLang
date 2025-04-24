import yfinance as yf

class BackTest:
    def __init__(self, executor):
        self.executor = executor
        self.tickers  = {}

    def run_backtest(self):
        # Step 2: Initialize
        portfolio_value = self.executor.capital
        cadence         = self.executor.conditionals["REBALANCE"][0]
        weights = {}
        benchmarks = {}
        start_date = None
        end_date   = None
        for ticker in self.executor.benchmarks:
            yf_ticker = yf.Ticker(ticker)

            start_date = self.executor.conditionals["AND"][0]
            end_date = self.executor.conditionals["AND"][1]
            benchmarks[ticker] = {
                "meta": yf_ticker.info,
                "history": yf_ticker.history(start=start_date, end=end_date, auto_adjust=True),
            }
            benchmarks[ticker]["daily_return"] = \
                    benchmarks[ticker]["history"]["Close"].pct_change()
            benchmarks[ticker]["daily_return"].dropna(inplace=True)

            benchmarks[ticker]["cap_return"]  = portfolio_value
            benchmarks[ticker]["cap_history"] = []
            for f_return in benchmarks[ticker]["daily_return"]:
                benchmarks[ticker]["cap_return"] *= (1 + f_return)
                benchmarks[ticker]["cap_history"].append(benchmarks[ticker]["cap_return"])

        for ticker, allocation in zip(self.executor.portfolio["tickers"],
                                      self.executor.portfolio["allocations"]):
            yf_ticker = yf.Ticker(ticker)

            start_date = self.executor.conditionals["AND"][0]
            end_date = self.executor.conditionals["AND"][1]

            self.tickers[ticker] = {
                "meta": yf_ticker.info,
                "history": yf_ticker.history(start=start_date, end=end_date, auto_adjust=True),
            }

            self.tickers[ticker]["daily_return"] = \
                    self.tickers[ticker]["history"]["Close"].pct_change()

            self.tickers[ticker]["daily_return"].dropna(inplace=True)

            weights[ticker] = float(allocation/100)

        print("==Portfolio==")
        print(weights)
        print("=============")

        print("== Test Against==")
        print(self.executor.benchmarks)
        print("=================")

        asset_values = {asset: self.executor.capital * weights[asset] for asset in weights}
        portfolio_history = {}
        rebalance_interval_days = cadence
        days_since_last_rebalance = rebalance_interval_days  # force rebalance on first day

        trading_days = float('inf')
        for ticker in self.tickers.keys():
            trading_days = min(trading_days,
               len(self.tickers[list(self.tickers.keys())[0]]["history"]))

        # Step 3: Loop through trading days
        for date in range(0, int(trading_days)):
            # Step 4: Update each asset's value based on return
            for asset in asset_values:
                if date >= len(self.tickers[asset]["daily_return"]):
                    break
                asset_values[asset] *= (1 + float(weights[asset]) * \
                    float(self.tickers[asset]["daily_return"].iloc[date])
                )

            # Step 5: Rebalance if needed
            days_since_last_rebalance += 1
            if days_since_last_rebalance >= rebalance_interval_days:
                total_value = sum(asset_values.values())
                for asset in asset_values:
                    asset_values[asset] = total_value * weights[asset]
                days_since_last_rebalance = 0

            # Step 6: Store portfolio value
            portfolio_value = sum(asset_values.values())
            portfolio_history[date] = portfolio_value

        print(portfolio_value)
        print(self.percent_return(self.executor.capital, portfolio_value))

        if self.executor.plot:
            import matplotlib.pyplot as plt
            import pandas as pd

            dates = pd.date_range(start=start_date, end=end_date,
                                  periods=len(portfolio_history.values()))
            values = list(portfolio_history.values())

            plt.plot(dates, values)

            for val in benchmarks.keys():
                print("Plotting Benchmark ", val)
                print(len(benchmarks[val]["history"]["Close"]))
                print(len(dates))
                print(benchmarks[val]["cap_return"])

                plt.plot(dates[0:len(benchmarks[val]["cap_history"])], benchmarks[val]["cap_history"][0:len(benchmarks[val]["cap_history"])])

            plt.show()

    def percent_return(self, start, end):
        return round(100 * ((end - start)/start), 2)
