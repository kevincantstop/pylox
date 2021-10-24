from lexer import Lexer
import utils


class Lang:
    def __init__(self, file):
        self.hadError = False
        self.code = utils.load(file)

    def exec(self):
        lexer = Lexer(self.code)
        return lexer.tokenize()
