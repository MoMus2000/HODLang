from environment import Environment
from executor    import Executor
from tokens      import TokenType

class Interpreter:
    def __init__(self, parser):
        self.parser   = parser
        self.executor = Executor()
        self.env      = Environment()

    def interpret(self):
        for statement in self.parser.statements:
            statement.accept(self)
        print(self.executor)
        self.executor.execute()

    def visit_portfolio_statement(self, stmt):
        print("===Portfolio==")
        print(stmt.tickers)
        print(stmt.allocation)
        if sum(stmt.allocation) != 100:
            raise Exception("Invalid Portfolio Allocation - Should add to 100%")
        self.executor.portfolio = {
            "allocations": stmt.allocation,
            "tickers": stmt.tickers
        }
        print("==============")

    def visit_expression_statement(self, stmt):
        return stmt.expr.accept(self)

    def visit_capital_statement(self, stmt):
        print("==Capital==")
        print("$"+str(stmt.amount))
        self.executor.capital = stmt.amount
        print("===========")

    def visit_backtest_statement(self, stmt):
        stmt.expr.accept(self)

    def visit_binary_expression(self, expr):
        if expr.left.token_type == TokenType.DATE and expr.right.token_type == TokenType.DATE:
           self.executor.conditionals[expr.op.token_type.name] = [
            expr.left.token_val,
            expr.right.token_val
        ]

    def visit_rebalance_statement(self, expr):
        self.executor.conditionals["REBALANCE"] = [int(expr.num.token_val),
                                                   expr.interval.token_type.name]

    def visit_plot_statement(self, _):
        self.executor.plot = True

    def visit_benchmark_statement(self, stmt):
        self.executor.benchmarks= stmt.benchmarks

    def visit_var_statement(self, stmt):
        self.env.define(stmt.ident, stmt.value)

