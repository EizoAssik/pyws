# encoding=utf-8

from wslexer import Reader, Lexer, AssemblerReader
from assembler import Assembler
from style import STL
from wsbuiltin import WSLiteral


def compiler(src: str, style: dict=STL, strict=False):
    ins = []
    ins_buff = None
    for token in Lexer(Reader(src, style), strict):
        if hasattr(token, 'ARGS'):
            if token.ARGS == 0:
                ins.append(token())
            else:
                ins_buff = token
        if isinstance(token, WSLiteral):
            ins.append(ins_buff(token))
            ins_buff = None
    return ins


def disassembler(ins, sep=''):
    return sep.join(map(repr, ins))


def assembler(src, sep=';', arg_sep=';'):
    a = Assembler(AssemblerReader(src), arg_sep=arg_sep)
    return sep.join(a.src)
