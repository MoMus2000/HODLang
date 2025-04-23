class Statement:
    pass


class CapitalStatement:
    def __init__(self, amount):
        self.amount = amount

class PortfolioStatement:
    def __init__(self, tickers):
        self.tickers = tickers

class ExpressionStatement:
    def __init__(self, expr):
        self.expr = expr

