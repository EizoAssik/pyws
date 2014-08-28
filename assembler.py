# encoding=utf-8

import os
import wsbuiltin
from wsbuiltin import FlowOperation, LABEL, NUMBER

items = [getattr(wsbuiltin, name) for name in dir(wsbuiltin)]
ASSEMBLER_TABLE = {c.NAME: c for c in items if hasattr(c, 'NAME')}


class AssemblerReader(object):
    def __init__(self, source):
        if not isinstance(source, str):
            raise TypeError("{} is neither a string containing source code "
                            "nor a path to source file".format(str(source)))
        if os.path.exists(source):
            with open(source) as sf:
                source = sf.readlines()
        else:
            source = source.splitlines()
        self.source = source

    def __iter__(self):
        return iter(self.source)


class Assembler(object):
    def __init__(self, reader, arg_sep):
        self.reader = reader
        self.arg_sep = arg_sep
        self.src, self.tokens = self.tokenize()

    def tokenize(self):
        tokens = []
        src = []
        for line in self.reader:
            if line.lstrip().startswith('#'):
                continue
            ins, *remain = line.split()
            if ins not in ASSEMBLER_TABLE:
                raise SyntaxError
            ins = ASSEMBLER_TABLE[ins]
            if remain:
                if issubclass(ins, FlowOperation):
                    literal = Assembler.literal_label(remain)
                    val = LABEL(literal)
                else:
                    literal = Assembler.literal_number(remain)
                    val = NUMBER(literal)
                src.append(ins.SRC + self.arg_sep + literal + 'L')
                tokens.append(ins(val))
            else:
                tokens.append(ins())
                src.append(ins.SRC)
        return src, tokens

    @staticmethod
    def literal_number(remains):
        negative = False
        literal = remains[0]
        if literal.startswith('b'):
            literal = literal[1:]
        elif literal.startswith('0x'):
            literal = bin(int(literal[2:], base=16))[2:]
        else:
            if literal.startswith('-'):
                literal = literal[1:]
                negative = True
            literal = bin(int(literal))[2:]
        if negative:
            literal = '1' + literal.translate({ord('0'): '1', ord('1'): '0'})
        else:
            literal = '0' + literal
        return literal.translate({ord('0'): 'S', ord('1'): 'T'})

    @staticmethod
    def literal_label(remains):
        negative = False
        literal = remains[0]
        if literal.startswith('b'):
            literal = literal[1:]
        elif literal.startswith('0x'):
            literal = bin(int(literal[2:], base=16))[2:]
        else:
            if literal.startswith('-'):
                literal = literal[1:]
                negative = True
            literal = bin(int(literal))[2:]
        if negative:
            literal = '1' + literal.translate({ord('0'): '1', ord('1'): '0'})
        return literal.translate({ord('0'): 'S', ord('1'): 'T'})
