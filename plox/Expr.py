from Token import Token
from typing import Any


class Expr:
    """
    [abstract]
    Expr class
    """

    def accept(self, visitor) -> Any:
        pass


class Visitor:
    """
    [interface]
    Visitor class
    """

    def visitBinaryExpr(self, expr) -> Any:
        pass

    def visitGroupingExpr(self, expr) -> Any:
        pass

    def visitLiteralExpr(self, expr) -> Any:
        pass

    def visitUnaryExpr(self, expr) -> Any:
        pass


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visitBinaryExpr(self)


class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visitGroupingExpr(self)


class Literal(Expr):
    def __init__(self, value: object) -> None:
        self.value = value

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visitLiteralExpr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visitUnaryExpr(self)
