# encoding=utf-8

from wslexer import Lexer
from style import STL
from wstoken import IMP
from wsbuiltin import WSOperation


def wscompiler(src: str, style: dict=STL):
    lexer = Lexer(src, style)
    status = IMP
    label_buffer = []
    num_buffer = []
    literal = True
    ins = []
    for c in lexer:
        if isinstance(status, dict):
            result = status[c]
            if isinstance(result, tuple) and len(result) == 3:
                cls, args, literal = result
                ins.append(cls())
                status = IMP
                continue
            else:
                next_level, leaf = result
                status = leaf if leaf else next_level
        else:
            raise SyntaxError
    return ins


def disassembler(ins, sep=''):
    return sep.join(map(repr, ins))