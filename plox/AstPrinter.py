from typing import Any, List
from Lox import Lox
from Token import Token
from TokenType import TokenType
from Expr import *


class AstPrinter(Visitor):
    """
    AstPrinter class
    """

    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visitBinaryExpr(self, expr: Binary) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: Grouping) -> str:
        return self.__parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: Literal) -> str:
        return "nil" if expr.value == None else str(expr.value)

    def visitUnaryExpr(self, expr: Unary) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.right)

    def __parenthesize(self, name: str, *exprs: List[Expr]) -> str:
        build_str = f"({name}"

        for expr in exprs:
            build_str = f"{build_str} {expr.accept(self)}"

        return build_str + ")"

    @classmethod
    def main(cls) -> None:
        expr = Binary(
            Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
            Token(TokenType.STAR, "*", None, 1),
            Grouping(Literal(45.67)),
        )

        print(AstPrinter().print(expr))


if __name__ == "__main__":
    AstPrinter.main()
