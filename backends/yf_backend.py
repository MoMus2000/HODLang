import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yfinance as yf

import logging
from . import backtest

sns.set_theme()

class YFBackTest(backtest.BackTest):
    def __init__(self, executor):
        self.executor = executor
        self.set_portfolio(executor)
        if executor.debug == True:
            logging.basicConfig(level=logging.INFO)
            pass

    def rebalance(self, asset_values, weights):
        total_value = sum(asset_values.values())
        for asset in asset_values:
            asset_values[asset] = total_value * weights[asset]

    def set_portfolio(self, executor):
        if self.executor.plot is True:
            self.create_plot = True
        self.tickers           = {}
        self.starting_capital  = executor.capital
        self.portfolio_value   = executor.capital
        self.cadence           = executor.conditionals["REBALANCE"][0]
        self.start_date        = executor.conditionals["AND"][0]
        self.end_date          = executor.conditionals["AND"][1]
        self.benchmarks        = {}
        self.weights           = {}
        self.portfolio_history = {}
        # ---------------------------------------------------------- #

        if self.executor.benchmarks is not None:
            for ticker in self.executor.benchmarks:
                yf_ticker = yf.Ticker(ticker)

                start_date = self.executor.conditionals["AND"][0]
                end_date = self.executor.conditionals["AND"][1]
                self.benchmarks[ticker] = {
                    "meta": yf_ticker.info,
                    "history": yf_ticker.history(start=start_date, end=end_date, auto_adjust=True),
                }
                self.benchmarks[ticker]["daily_return"] = \
                        self.benchmarks[ticker]["history"]["Close"].pct_change().fillna(0)
                self.benchmarks[ticker]["daily_return"].dropna(inplace=True)

                self.benchmarks[ticker]["cap_return"]  = self.portfolio_value
                self.benchmarks[ticker]["cap_history"] = []
                for f_return in self.benchmarks[ticker]["daily_return"]:
                    self.benchmarks[ticker]["cap_return"] *= (1 + f_return)
                    self.benchmarks[ticker]["cap_history"].append(
                            self.benchmarks[ticker]["cap_return"])

        # ---------------------------------------------------------- #
        for ticker, allocation in zip(executor.portfolio["tickers"],
                                      executor.portfolio["allocations"]):
            yf_ticker = yf.Ticker(ticker)

            start_date = self.executor.conditionals["AND"][0]
            end_date = self.executor.conditionals["AND"][1]

            self.tickers[ticker] = {
                "meta": yf_ticker.info,
                "history": yf_ticker.history(start=start_date, end=end_date, auto_adjust=True),
            }

            self.tickers[ticker]["daily_return"] = \
                    self.tickers[ticker]["history"]["Close"].pct_change().fillna(0)

            self.tickers[ticker]["daily_return"].dropna(inplace=True)

            self.weights[ticker] = float(allocation/100)

        # ---------------------------------------------------------- #

        self.asset_values = {asset: executor.capital * self.weights[asset] for asset in
                             self.weights}
        self.portfolio_history = {}
        self.rebalance_interval_days = self.cadence

        trading_days = float('inf')
        for ticker in self.tickers.keys():
            trading_days = min(trading_days,
               len(self.tickers[list(self.tickers.keys())[0]]["history"]))

    def run_backtest(self):
        # Step 2: Initialize

        logging.info("==Portfolio==")
        logging.info(self.weights)
        logging.info("=============")

        logging.info("== Test Against==")
        logging.info(self.executor.benchmarks)
        logging.info("=================")

        days_since_last_rebalance = self.rebalance_interval_days  # force rebalance on first day

        trading_days = float('inf')
        for ticker in self.tickers.keys():
            trading_days = min(trading_days,
               len(self.tickers[list(self.tickers.keys())[0]]["history"]))

        # Step 3: Loop through trading days
        for date in range(0, int(trading_days)):
            # Step 4: Update each asset's value based on return
            for asset in self.asset_values:
                if date >= len(self.tickers[asset]["daily_return"]):
                    break
                self.asset_values[asset] *= (1 + float(self.weights[asset]) * \
                    float(self.tickers[asset]["daily_return"].iloc[date])
                )

            # Step 5: Rebalance if needed
            days_since_last_rebalance += 1
            if days_since_last_rebalance >= self.rebalance_interval_days:
                self.rebalance(self.asset_values, self.weights)
                days_since_last_rebalance = 0

            # Step 6: Store portfolio value
            self.portfolio_value = sum(self.asset_values.values())
            self.portfolio_history[date] = self.portfolio_value

        logging.info(self.percent_return(self.starting_capital, self.portfolio_value))

        if self.create_plot:

            dates = pd.date_range(start=self.start_date, end=self.end_date,
                                  periods=len(self.portfolio_history.values()))
            values = list(self.portfolio_history.values())

            label = ""
            for ticker, allocation in zip(
                    self.executor.portfolio["tickers"],
                    self.executor.portfolio["allocations"]
                ):
                label += f"Portfolio: {ticker}({allocation}) "


            plt.plot(dates, values, label=label)

            for val in self.benchmarks.keys():
                plt.plot(
                    dates[0:len(self.benchmarks[val]["cap_history"])],
                    self.benchmarks[val]["cap_history"][0:len(self.benchmarks[val]["cap_history"])],
                    label=val
                )

            plt.title("HODL")
            plt.legend()
            plt.tight_layout()
            plt.style.use('fivethirtyeight')
            plt.show()

    def percent_return(self, start, end):
        return round(100 * ((end - start)/start), 2)

