# encoding=utf-8

from wslexer import Reader, Lexer
from style import STL
from wsbuiltin import WSOperation


def wscompiler(src:str, style:dict=STL):
    ins = []
    for token in Lexer(Reader(src, style)):
        if issubclass(token, WSOperation):
            ins.append(token())
    return ins


def disassembler(ins, sep=''):
    return sep.join(map(repr, ins))