from visitor import Visitor
from expr import *


class ExprPrinter(Visitor):
    def visit_binary(self, expr: Binary):
        print("(", end='')
        print(expr.operator.literal, end='')
        self.visit(expr.left)
        self.visit(expr.right)
        print(")", end='')

    def visit_grouping(self, expr: Grouping):
        print("(", end='')
        self.visit(expr.expr)
        print(")", end='')

    def visit_literal(self, expr: Literal):
        print(expr.value, end='')

    def visit_unary(self, expr: Unary):
        print("(", end='')
        print(expr.operator.literal, end='')
        self.visit(expr.right)
        print(")", end='')

    def print(self, expr: Expr):
        expr.accept(self)
