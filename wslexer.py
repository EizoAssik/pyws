# encoding=utf-8
import os
from style import STL
from wstoken import IMP
from wsbuiltin import END


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

    def __init__(self, reader: Reader, strict=False):
        self.reader = reader
        self.strict = strict
        self.ins = self.lex()

    def lex(self):
        found_end = False
        status = IMP
        literal_buffer = []
        literal = None
        ins = []
        for c in self.reader:
            if literal is not None:
                if c != 'L':
                    literal_buffer.append(c)
                else:
                    ins.append(literal(''.join(literal_buffer)))
                    # use this instead of literal_buffer.clear()
                    # so that this will work in PyPy3
                    literal_buffer = []
                    literal = None
                continue
            if isinstance(status, dict):
                result = status[c]
                if isinstance(result, tuple) and len(result) == 3:
                    cls, args, literal = result
                    if cls is END:
                        found_end = True
                    ins.append(cls)
                    status = IMP
                else:
                    next_level, leaf = result
                    if leaf and not isinstance(leaf, dict):
                        cls, args, literal = leaf
                        if cls is END:
                            found_end = True
                        ins.append(cls)
                        status = IMP
                    elif leaf and isinstance(leaf, dict):
                        status = leaf
                    else:
                        status = next_level
            else:
                raise SyntaxError
        if self.strict and any((literal_buffer, literal,
                                status != IMP,
                                not found_end)):
            raise SyntaxError("Not end at L-[LF][LF] END")
        return ins

    def __iter__(self):
        return iter(self.ins)








