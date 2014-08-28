# encoding=utf-8

import argparse
import style as wsstyle

from wslexer import Reader, Lexer
from assembler import Assembler, AssemblerReader
from engine import PYWSEngine, PYFN_MAP
from wsbuiltin import WSLiteral, LABEL


def compiler(src: str, style: dict=wsstyle.STL, strict=False):
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
    return sep.join(a.src), a.ins


def main():
    argparser = argparse.ArgumentParser(
        description="PYWS, a WhiteSpace interpreter in Python.")
    argparser.add_argument('source', help='source string or file')
    argparser.add_argument('-A', dest='assemble', action='store_true',
                           default=False,
                           help='if given, use assembler instant of compiler')
    argparser.add_argument('--strict', dest='strict', default=False,
                           action='store_true',
                           help='use strict mode, default: False')
    argparser.add_argument('--style', dest='style', default='STL',
                           help='code style, STL, ORIGIN or GMH')
    argparser.add_argument('--sep', dest='sep', default=';',
                           help='separator for assembled code between operator')
    argparser.add_argument('--arg-sep', dest='arg_sep', default=';',
                           help='separator for assembled code between argument')
    args = argparser.parse_args()
    if args.assemble:
        code, ins = assembler(args.source, args.sep, args.arg_sep)
        print('=' * 16)
        print('Compile result:')
        print(code)
        stack, heap = PYWSEngine(ins).run()
        print('\n' + '=' * 16)
        print('STACK: ', stack)
        print('HEAP: ', heap)
    else:
        if args.style in dir(wsstyle):
            style = getattr(wsstyle, args.style)
        else:
            style = wsstyle.STL
        ins = compiler(args.source, style, args.strict)
        stack, heap = PYWSEngine(ins).run()
        print('=' * 16)
        print('STACK: ', stack)
        print('HEAP: ', heap)


def wsfunction(style=wsstyle.STL, strict=False, debug=False,
               stack_only=False, heap_only=False, stack_heap=False,
               ret_top=True):
    def _wsdef(func):
        src = func.__doc__
        ins = compiler(src, style, strict)

        def _wsfunc(*args, **kwargs):
            engine = PYWSEngine(ins, stack=args, heap=kwargs)
            stack, heap = engine.run(debug=debug)
            if stack_only:
                return stack
            if heap_only:
                return heap
            if stack_heap:
                return stack, heap
            if ret_top:
                return stack.pop()

        return _wsfunc

    return _wsdef


def wsmark(label):
    l = LABEL(label)

    def _wsmark(func):
        PYFN_MAP[l] = func
        return func

    return _wsmark


if __name__ == '__main__':
    main()