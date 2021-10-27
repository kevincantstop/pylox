from tokens import TokenType
from expr import Binary, Literal, Grouping, Unary
from err import LoxError


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        return self.expression()

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            op = self.previous()
            right = self.comparison()

            expr = Binary(expr, op, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match([TokenType.GREATER, TokenType.GREATER_EQUAL]):
            op = self.previous()
            right = self.term()
            expr = Binary(expr, op, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match([TokenType.MINUS, TokenType.PLUS]):
            op = self.previous()
            right = self.factor()
            expr = Binary(expr, op, right)

        return expr

    def factor(self):
        expr = self.unary()
        while self.match([TokenType.SLASH, TokenType.STAR]):
            op = self.previous()
            right = self.unary()
            expr = Binary(expr, op, right)

        return expr

    def unary(self):
        if self.match([TokenType.BANG, TokenType.MINUS]):
            op = self.previous()
            right = self.unary()
            return Unary(op, right)

        return self.primary()

    def primary(self):
        if self.match([TokenType.FALSE]):
            return Literal(False)
        if self.match([TokenType.TRUE]):
            return Literal(True)

        if self.match([TokenType.NUMBER, TokenType.STRING]):
            return Literal(self.previous())

        if self.match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
            return Grouping(expr)

        raise LoxError("Expect expression at line: {}".format(self.peek().line))

    def consume(self, token_type, msg):
        if self.check(token_type):
            return self.advance()

        raise LoxError(msg + " at line: {}".format(self.peek().line))

    def match(self, types):
        for t in types:
            if self.check(t):
                self.advance()
                return True

        return False

    def check(self, token_type):
        if self.is_end():
            return False
        return self.peek().type == token_type

    def advance(self):
        if not self.is_end():
            self.current += 1
        return self.previous()

    def is_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
