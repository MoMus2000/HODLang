from abc import ABC, abstractmethod

class Statement(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def accept(self, visitor):
        pass

class CapitalStatement(Statement):
    def __init__(self, amount):
        self.amount = amount

    def accept(self, visitor):
        return visitor.visit_capital_statement(self)

class PortfolioStatement(Statement):
    def __init__(self, tickers, allocation):
        self.tickers    = tickers
        self.allocation = allocation

    def accept(self, visitor):
        return visitor.visit_portfolio_statement(self)

class ExpressionStatement(Statement):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_expression_statement(self)

class BackTestStatement(Statement):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_backtest_statement(self)

class RebalanceStatement(Statement):
    def __init__(self, num, interval):
        self.num      = num
        self.interval = interval

    def accept(self, visitor):
        return visitor.visit_rebalance_statement(self)

