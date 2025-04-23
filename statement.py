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
        visitor.visit_capital_statement(self)

class PortfolioStatement(Statement):
    def __init__(self, tickers):
        self.tickers = tickers

    def accept(self, visitor):
        visitor.visit_portfolio_statement(self)

class ExpressionStatement(Statement):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_expression_statement(self)

class BackTestStatement(Statement):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_backtest_statement(self)


