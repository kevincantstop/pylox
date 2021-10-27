from __future__ import absolute_import
from lexer import Lexer
from parse import Parser
import utils


class Lang:
    def __init__(self, file):
        self.hadError = False
        self.code = utils.load(file)

    def exec(self):
        lexer = Lexer(self.code)
        tokens = lexer.tokenize()

        p = Parser(tokens)
        return p.parse()
