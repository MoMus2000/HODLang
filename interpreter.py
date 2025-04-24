class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def interpret(self):
        for statement in self.parser.statements:
            statement.accept(self)

    def visit_portfolio_statement(self, stmt):
        print("===Portfolio==")
        print(stmt.tickers)
        print(stmt.allocation)
        if sum(stmt.allocation) != 100:
            raise Exception("Invalid Portfolio Allocation - Should add to 100%")
        print("==============")

    def visit_expression_statement(self, stmt):
        print("==Expr==")
        stmt.expr.accept(self)
        print("========")

    def visit_capital_statement(self, stmt):
        print("==Capital==")
        print("$"+stmt.amount)
        print("===========")

    def visit_backtest_statement(self, stmt):
        print("==BackTest==")
        stmt.expr.accept(self)
        print("============")

    def visit_binary_expression(self, expr):
        print("D1: ", expr.left)
        print("OP: ", expr.op)
        print("D2: ", expr.right)

