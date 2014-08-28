# encoding=utf-8

import os

import wsbuiltin
from wsbuiltin import FlowOperation, LABEL, NUMBER
import sugar


builtin_items = [getattr(wsbuiltin, name) for name in dir(wsbuiltin)]
ASSEMBLER_TABLE = {c.NAME: c for c in builtin_items if hasattr(c, 'NAME')}
sugar_items = [getattr(sugar, name) for name in dir(sugar)]
SUGAR_TABLE = {c.NAME: c for c in sugar_items if hasattr(c, 'NAME')}


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
        self.source = AssemblerReader.preprocess(source)

    def __iter__(self):
        return iter(self.source)

    @classmethod
    def preprocess(cls, raw):
        src = []
        for line in raw:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            ins, *remains = line.split(sep=' ', maxsplit=1)
            if remains:
                if '#' in remains:
                    remains = remains[:remains.index('#')]
                remains = list(filter(lambda x: not x.startswith('#'), remains))
                remain = ' '.join(remains)
            else:
                remain = None
            src.append((ins, remain))

        return src


class Assembler(object):
    def __init__(self, reader, arg_sep):
        self.reader = reader
        self.source = reader.source
        self.arg_sep = arg_sep
        self.src, self.ins = self.tokenize()

    def tokenize(self):
        tokens = []
        src = []
        pos = 0
        while pos < len(self.source):
            ins, remain = self.source[pos]
            if ins in SUGAR_TABLE:
                expanded_src = SUGAR_TABLE[ins].expand(remain)
                for eline in reversed(expanded_src):
                    self.source.insert(pos + 1, eline)
                pos += 1
                continue
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
            pos += 1
        return src, tokens

    @staticmethod
    def literal_number(literal):
        negative = False
        if literal.startswith('b'):
            literal = literal[1:]
        if literal.startswith('\''):
            literal = bin(ord(literal[1]))[2:]
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
    def literal_label(literal):
        negative = False
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
