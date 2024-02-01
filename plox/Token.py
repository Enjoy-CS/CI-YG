from TokenType import *


class Token:
    """_summary_
    Token class
    """

    def __init__(
        self, token_type: TokenType, lexeme: str, literal: object, line: int
    ) -> None:
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def to_string(self) -> str:
        return f"{self.token_type}, {self.lexeme}, {self.literal}"
