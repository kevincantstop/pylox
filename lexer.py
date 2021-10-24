from tokens import Token, TokenType


class Lexer:
    def __init__(self, code):
        self.src = code

        self.line = 1
        self.start = 0
        self.current = 0

        self.values = []
        self.keywords = {
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

    def tokenize(self):
        while not self.is_end():
            self.start = self.current
            self.scan()

        self.values.append(Token(TokenType.EOF, None, None, self.line))
        return self.values

    def scan(self):
        c = self.advance()

        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '*':
            self.add_token(TokenType.STAR)
        elif c == '!':
            if self.match('='):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif c == '=':
            if self.match('='):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)
        elif c == '<':
            if self.match('='):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif c == '>':
            if self.match('='):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' or (not self.is_end()):
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == '"':
            self.string()
        elif c == '\n':
            self.line += 1
        elif c == '\r' or c == '\t':
            pass
        else:
            if self.is_digit(c):
                self.number()
            elif self.is_alpha(c):
                self.identifier()

            print('Unrecognized character: {}'.format(self.line))

    def string(self):
        while self.peek() != '"':
            self.advance()
        self.advance()
        v = self.src[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, v, v)

    def number(self):
        while self.is_digit(self.peek()) or (self.peek() == '.' and self.is_digit(self.peek_next())):
            self.advance()
        self.add_token(TokenType.NUMBER, self.src[self.start: self.current])

    def identifier(self):
        while self.is_alphanum(self.peek()):
            self.advance()

        v = self.src[self.start: self.current]
        if v in self.keywords:
            self.add_token(self.keywords[v], v)
        else:
            self.add_token(TokenType.IDENTIFIER, v)

    def is_end(self):
        return self.current >= len(self.src)

    def advance(self):
        c = self.src[self.current]
        self.current += 1
        return c

    def add_token(self, token_type, literal=None, val=None):
        val = self.src[self.start: self.current] if val is None else val
        self.values.append(Token(token_type, literal, val, self.line))

    def match(self, char):
        if self.is_end() or self.src[self.current] != char:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.is_end():
            return '\0'
        return self.src[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.src):
            return '\0'
        return self.src[self.current + 1]

    def is_digit(self, c):
        return c.isdigit()

    def is_alpha(self, c):
        return c.isalpha()

    def is_alphanum(self, c):
        return c.isalnum() or c == '_'
