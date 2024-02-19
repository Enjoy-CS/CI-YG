from Token import Token
from TokenType import TokenType
from Expr import Expr, Binary, Grouping, Literal, Unary
from typing import List, Callable


class Parser:
    """
    Parser class
    """

    class ParseError(RuntimeError):
        pass

    def __init__(self, tokens: List[Token], lox_error: Callable) -> None:
        self.__tokens = tokens
        self.__current = 0
        self.__lox_error = lox_error

    def pasre(self) -> Expr:
        try:
            return self.__expression()
        except Parser.ParseError:  # 주어진 토큰을 다 안쓰는 경우도 처리가 필요 함
            return None

    def __expression(self) -> Expr:
        return self.__equality()

    def __equality(self) -> Expr:
        expr = self.__comparison()

        while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.__previous()
            right = self.__comparison()
            expr = Binary(expr, operator, right)

        return expr

    def __comparison(self) -> Expr:
        expr = self.__term()

        while self.__match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.__previous()
            right = self.__term()
            expr = Binary(expr, operator, right)

        return expr

    def __term(self) -> Expr:
        expr = self.__factor()

        while self.__match(TokenType.MINUS, TokenType.PLUS):
            operator = self.__previous()
            right = self.__factor()
            expr = Binary(expr, operator, right)

        return expr

    def __factor(self) -> Expr:
        expr = self.__unary()

        while self.__match(TokenType.SLASH, TokenType.STAR):
            operator = self.__previous()
            right = self.__unary()
            expr = Binary(expr, operator, right)

        return expr

    def __unary(self) -> Expr:
        if self.__match(TokenType.BANG, TokenType.MINUS):
            operator = self.__previous()
            right = self.__unary()
            return Unary(operator, right)

        return self.__primary()

    def __primary(self) -> Expr:
        if self.__match(TokenType.FALSE):
            return Literal(False)
        if self.__match(TokenType.TRUE):
            return Literal(True)
        if self.__match(TokenType.NIL):
            return Literal(None)
        if self.__match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.__previous().literal)

        if self.__match(TokenType.LEFT_PAREN):
            expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.__error(self.__peek(), "Expect expression.")

    def __match(self, *token_types: List[TokenType]) -> bool:
        for token_type in token_types:
            if self.__check(token_type):
                self.__advance()
                return True

        return False

    def __consume(self, token_type: TokenType, message: str) -> Token:
        if self.__check(token_type):
            return self.__advance()

        raise self.__error(self.__peek(), message)

    def __check(self, token_type: TokenType) -> bool:
        if self.__isAtEnd():
            return False
        return self.__peek().token_type == token_type

    def __advance(self) -> Token:
        if not self.__isAtEnd():
            self.__current += 1
        return self.__previous()

    def __isAtEnd(self) -> bool:
        return self.__peek().token_type == TokenType.EOF

    def __peek(self) -> Token:
        return self.__tokens[self.__current]

    def __previous(self) -> Token:
        return self.__tokens[self.__current - 1]

    def __error(self, token: Token, message: str) -> ParseError:
        self.__lox_error(token=token, message=message)
        return Parser.ParseError("parse error")

    def __synchronize(self) -> None:
        self.__advance()

        while not self.__isAtEnd():
            if self.__previous.token_type == TokenType.SEMICOLON:
                return

            match self.__peek().token_type:
                case (
                    TokenType.CLASS
                    | TokenType.FUN
                    | TokenType.VAR
                    | TokenType.FOR
                    | TokenType.IF
                    | TokenType.WHILE
                    | TokenType.PRINT
                    | TokenType.RETURN
                ):
                    return

            self.__advance()
