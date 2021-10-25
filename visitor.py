class Visitor:
    def visit(self, expr):
        func = getattr(self, 'visit_{}'.format(type(expr).__name__.lower()))
        func(expr)
