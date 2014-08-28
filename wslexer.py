# encoding=utf-8
import os
from style import STL
from wstoken import IMP


class Reader(object):
    """
    This is the source code reader for WhiteSpace.
    """

    def __init__(self, source: str, style: dict=STL):
        if not isinstance(source, str):
            raise TypeError("{} is neither a string containing source code "
                            "nor a path to source file".format(str(source)))
        if os.path.exists(source):
            with open(source) as sf:
                source = sf.read()
        self.source = source
        self.style = style
        self.doc = filter(lambda c: c not in self.style, source)
        self.code = tuple(filter(None,
                                 map(lambda c: self.style.get(c, None),
                                     self.source)))

    def __iter__(self):
        return iter(self.code)


class Lexer(object):
    """
    This is the lexer for WhiteSpace
    """

    def __init__(self, reader: Reader):
        self.reader = reader
        self.ins = self.lex()

    def lex(self):
        status = IMP
        label_buffer = []
        num_buffer = []
        literal = True
        ins = []
        for c in self.reader:
            if isinstance(status, dict):
                result = status[c]
                if isinstance(result, tuple) and len(result) == 3:
                    cls, args, literal = result
                    ins.append(cls)
                    status = IMP
                    continue
                else:
                    next_level, leaf = result
                    status = leaf if leaf else next_level
            else:
                raise SyntaxError
        return ins

    def __iter__(self):
        return iter(self.ins)
