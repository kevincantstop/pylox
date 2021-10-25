from lang import Lang
from expr import *
from printer import ExprPrinter
from tokens import *


def print_expr():
    e = Binary(
        Unary(
            Token(TokenType.MINUS, "-", "-", 0),
            Literal(123)
        ),
        Token(TokenType.STAR, "*", "*", 0),
        Grouping(Literal(45.67))
    )

    ExprPrinter().print(e)


if __name__ == '__main__':
    l = Lang("prog/test.lox")
    v = l.exec()

    print_expr()
