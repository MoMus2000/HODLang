from token import TokenType
from expression import (
    BinaryExpression
)
from statement import (
    CapitalStatement,
    PortfolioStatement,
    ExpressionStatement,
    BackTestStatement
)

class Parser:
    def __init__(self, lexer):
        self.lexer  = lexer
        self.tokens = lexer.tokens
        self.current = 0
        self.statements = []

        self.parse()
    
    def parse(self):
        while not self.is_at_end():
            statement = self.parse_statements()
            if statement is not None:
                self.statements.append(statement)

    def parse_statements(self):
        return self.declaration()

    def declaration(self):
        if self.match(TokenType.CAPITAL):
            self.consume(TokenType.COLON, "COLON")
            amount = self.consume(TokenType.DOLLAR, "Get amount").token_val
            return CapitalStatement(amount)

        if self.match(TokenType.PORTFOLIO):
            self.consume(TokenType.COLON, "COLON")
            tickers = self.parse_tickers()
            return PortfolioStatement(tickers)

        if self.match(TokenType.BACKTEST):
            expr = self.expression_statement()
            return BackTestStatement(expr)

        return self.statement()

    def comparision(self):
        if self.match(TokenType.BETWEEN):
            d1 = self.consume(TokenType.DATE, "Expected date")
            if not self.match(TokenType.AND, TokenType.OR):
                raise Exception("Unsupported Operator")
            op = self.previous()
            d2 = self.consume(TokenType.DATE, "Expected date")

            return ExpressionStatement(BinaryExpression(
                d1, op, d2
            ))

        self.advance()

    def parse_tickers(self):
        tickers = []
        if self.peek().token_type == TokenType.IDENTIFIER:
            while self.match(TokenType.IDENTIFIER):
                ticker = self.previous()
                tickers.append(ticker.token_val)
                if self.check(TokenType.COMMA):
                    self.consume(TokenType.COMMA, "Consume comma")

        return tickers


    def match(self, *ttype):
        for token in ttype:
            if self.check(token):
                self.advance()
                return True
        return False

    def expression_statement(self):
        return self.comparision()

    def statement(self):
        return self.expression_statement()

    def previous(self):
        return self.tokens[self.current-1]

    def peek(self):
        return self.tokens[self.current]

    def consume(self, token_type, msg):
        if self.check(token_type):
            return self.advance()
        raise Exception(msg)

    def check(self, ttype):
        return self.peek().token_type == ttype

    def advance(self):
        if not self.is_at_end:
            raise Exception("At the end of file ..")
        t = self.tokens[self.current]
        self.current += 1
        return t

    def is_at_end(self):
        return self.peek().token_type == TokenType.EOF

