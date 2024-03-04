from beartype import beartype


@beartype
class switch:

    def __init__(self, variable: any, comparator: any = lambda x, y: x == y, strict: bool = True):
        self.variable = variable
        self.matched = False
        self.matching = False
        if comparator:
            self.comparator = comparator
        else:
            self.comparator = lambda x, y: x == y
        self.strict = strict

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def case(self, expr: any, break_: bool=False):
        if self.strict:
            if self.matched:
                return False
        if self.matching or self.comparator(self.variable, expr):
            if not break_:
                self.matching = True
            else:
                self.matched = True
                self.matching = False
            return True
        else:
            return False

    def default(self):
        return not self.matched and not self.matching
