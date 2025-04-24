from enum import Enum, auto

class TokenType(Enum):
    IDENTIFIER  = auto()
    PORTFOLIO   = auto()
    CAPITAL     = auto()
    IF          = auto()
    ELSE        = auto()
    COLON       = auto()
    COMMA       = auto()
    BACKTEST    = auto()
    FROM        = auto()
    BETWEEN     = auto()
    DOLLAR      = auto()
    NUMBER      = auto()
    PLUS        = auto()
    MINUS       = auto()
    STAR        = auto()
    SLASH       = auto()
    REBALANCE   = auto()
    OVER        = auto()
    TIME        = auto()
    LEFT_PAREN  = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE  = auto()
    RIGHT_BRACE = auto()
    DATE        = auto()
    AND         = auto()
    RUN         = auto()
    OR          = auto()
    PLOT        = auto()
    EOF         = auto()

class Token:
    def __init__(self, token_type, token_val=""):
        self.token_type = token_type
        self.token_val  = token_val

    def __str__(self) -> str:
        return f"Token Type: {self.token_type}, Token Val: {self.token_val}"

