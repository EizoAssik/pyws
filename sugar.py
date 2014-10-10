# encoding=utf-8
import re


class SyntaxSugar(object):
    NAME = "@"

    @staticmethod
    def expand(arg):
        pass


class PUSHS(SyntaxSugar):
    NAME = "PUSHS"

    @staticmethod
    def expand(arg: str):
        rev = False
        arg = arg.strip()
        if arg.startswith('~'):
            arg = arg[1:]
            rev = True
        if re.match(r"\[ ?((-?\d+ ?, ?)( ?))*-?\d+ ?\]", arg):
            ints = eval(arg)
            if rev:
                ints = ints[::-1]
            return list(map(lambda i: ('PUSH', str(i)), ints))
        if re.match(r"\".*\"", arg):
            arg = arg.strip('\"')
            if rev:
                arg = arg[::-1]
            return list(map(lambda i: ('PUSH', str(ord(i))), arg))
        raise SyntaxError("Cannot expand PUSHS {}".format(arg))