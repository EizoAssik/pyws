# encoding=utf-8
import os
from style import STL


class Lexer(object):
    """
    This is the lexer for WhiteSpace.
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
