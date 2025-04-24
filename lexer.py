from token import Token, TokenType

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.current     = 0
        self.start       = 0
        self.tokens      = []
        self.keywords    = {
          "PORTFOLIO": TokenType.PORTFOLIO,
          "CAPITAL":   TokenType.CAPITAL,
          "BACKTEST":  TokenType.BACKTEST,
          "BETWEEN":   TokenType.BETWEEN,
          "REBALANCE": TokenType.REBALANCE,
          "AND":       TokenType.AND,
          "OR":        TokenType.OR,
          "PLOT":      TokenType.PLOT
        }

        self.scan_tokens()

    def scan_tokens(self):
        while not self.is_at_end():
            self.scan_token()
        self.add_token(Token(TokenType.EOF, None))

    def add_token(self, t):
        self.tokens.append(t)

    def scan_token(self):
        c = self.advance()
        if c == "$":
            self.add_token(Token(token_type=TokenType.DOLLAR, token_val=self.number()))

        elif c == ":":
            self.add_token(Token(token_type=TokenType.COLON, token_val=None))

        elif c == "(":
            self.add_token(Token(token_type=TokenType.LEFT_PAREN, token_val=None))

        elif c == ")":
            self.add_token(Token(token_type=TokenType.RIGHT_PAREN, token_val=None))
        
        elif c == ",":
            self.add_token(Token(token_type=TokenType.COMMA, token_val=None))

        elif self.is_string(c):
            string = self.string()
            if string.strip() in self.keywords:
                token = self.keywords[string]
                self.add_token(Token(token_type=token, token_val=None))
            else:
                self.add_token(Token(token_type=TokenType.IDENTIFIER, token_val=string))

        elif c.isnumeric():
            self.add_token(Token(token_type=TokenType.DATE, token_val=self.date()))


    def date(self):
        num = ""+self.source_code[self.current-1]
        while True:
            c = self.advance()
            if not c.isnumeric() and c != "-":
                self.current -= 1
                break
            num += c
        return num

    
    def number(self):
        num = ""
        while True:
            c = self.advance()
            if not c.isnumeric() and c != ".":
                break
            num += c
        return num

    def string(self):
        str_val = ""+self.source_code[self.current-1]
        while True:
            c = self.source_code[self.current]
            if not c.isalpha():
                break
            str_val += c
            self.advance()
        return str_val
    
    def is_string(self, c):
        return c.isalpha()

    def advance(self):
        c = self.source_code[self.current]
        self.current += 1
        return c
     
    def is_at_end(self):
        if self.current < len(self.source_code):
            return False
        return True
    
