from Token import *
from TokenType import *
from Lox import *


class Scanner:
    """
    Scanner class
    """

    keyword_dic = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str) -> None:
        self.__source = source
        self.__tokens = list()
        self.__start = 0
        self.__current = 0
        self.__line = 1

    def scan_tokens(self) -> list:
        while not self.__is_at_end():
            self.__start = self.__current
            self.__scan_token()

        self.__tokens.append(Token(TokenType.EOF, "", None, self.__line))
        return self.__tokens

    def __scan_token(self) -> None:
        c = self.__advance()

        match c:
            case "(":
                self.__add_token(TokenType.LEFT_PAREN)
            case ")":
                self.__add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.__add_token(TokenType.LEFT_BRACE)
            case "}":
                self.__add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.__add_token(TokenType.COMMA)
            case ".":
                self.__add_token(TokenType.DOT)
            case "-":
                self.__add_token(TokenType.MINUS)
            case "+":
                self.__add_token(TokenType.PLUS)
            case ";":
                self.__add_token(TokenType.SEMICOLON)
            case "*":
                self.__add_token(TokenType.STAR)
            case "!":
                self.__add_token(
                    TokenType.BANG_EQUAL if self.__match("=") else TokenType.BANG
                )
            case "=":
                self.__add_token(
                    TokenType.EQUAL_EQUAL if self.__match("=") else TokenType.EQUAL
                )
            case "<":
                self.__add_token(
                    TokenType.LESS_EQUAL if self.__match("=") else TokenType.LESS
                )
            case ">":
                self.__add_token(
                    TokenType.GREATER_EQUAL if self.__match("=") else TokenType.GREATER
                )
            case "/":
                if self.__match("/"):
                    while self.__peek() != "\n" and not self.__is_at_end():
                        self.__advance()
                else:
                    self.__add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.__line += 1
            case '"':
                self.__string()
            case _:
                if c.isdigit():
                    self.__number()
                elif c.isalpha() or c == "_":
                    self.__identifier()
                else:
                    Lox.error(self.__line, "Unexpected character.")

    def __add_token(self, tokenType: TokenType, literal: object = None) -> None:
        self.__tokens.append(
            Token(
                tokenType,
                self.__source[self.__start : self.__current],
                literal,
                self.__line,
            )
        )

    def __is_at_end(self) -> bool:
        return self.__current >= len(self.__source)

    def __match(self, expected: str) -> bool:
        if self.__is_at_end():
            return False
        if self.__source[self.__current] != expected:
            return False

        self.__current += 1
        return True

    def __advance(self) -> str:
        c = self.__source[self.__current]
        self.__current += 1
        return c

    def __peek(self) -> str:
        if self.__is_at_end():
            return "\0"
        return self.__source[self.__current]

    def __peek_next(self) -> str:
        if self.__current + 1 >= len(self.__source):
            return "\0"
        return self.__source[self.__current + 1]

    def __string(self) -> None:
        while self.__peek() != '"' and not self.__is_at_end():
            if self.__peek() == "\n":
                self.__line += 1
            self.__advance()

        if self.__is_at_end():
            Lox.error(self.__line, "Unterminated string.")
            return

        self.__advance()

        self.__add_token(
            TokenType.STRING, self.__source[self.__start + 1 : self.__current - 1]
        )

    def __number(self) -> None:
        while self.__peek().isdigit():
            self.__advance()

        if self.__peek() == "." and self.__peek_next().isdigit():
            self.__advance()

            while self.__peek().isdigit():
                self.__advance()

        self.__add_token(
            TokenType.NUMBER, float(self.__source[self.__start : self.__current])
        )

    def __identifier(self) -> None:
        while self.__peek().isalnum() or self.__peek() == "_":
            self.__advance()

        token_type = Scanner.keyword_dic.get(
            self.__source[self.__start : self.__current]
        )
        if not token_type:
            token_type = TokenType.IDENTIFIER
        self.__add_token(token_type)
