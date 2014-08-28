# encoding=utf-8

from wslexer import Reader, Lexer
from style import STL
from wsbuiltin import WSOperation, WSLiteral


def wscompiler(src: str, style: dict=STL, strict=False):
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