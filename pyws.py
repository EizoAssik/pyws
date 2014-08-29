# encoding=utf-8

import argparse
import style as wsstyle

from wslexer import Reader, Lexer
from assembler import Assembler, AssemblerReader
from engine import PYWSEngine, PYFN_MAP
from wsbuiltin import WSLiteral, LABEL


def compiler(src: str, style: dict=wsstyle.STL, strict=False):
    """
    Compile STL codes into callable WSOperations
    """
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
    """
    Give a list of callable WSOperators,
    return the wsa notations, which can be read back again
    by assembler
    """
    return sep.join(map(repr, ins))


def assembler(src, sep=';', arg_sep=';'):
    """
    Give a wsa file's path or a string contains wsa,
    return 2 values, STL code and instructions
    """
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
    """
    This decorator will make a callable function in Python, which is written in
    WhiteSpace.

    The flags are defined below:
    :style code style, STL, ORIGIN, or GMH. default: STL
    :strict if set to True, program must end at LLL. default: False
    :debug if set to True, program will run in debug mode. default: False
    :ret_top return the top of the stack after running the code. default: True
    :stack_only only return the whole stack. default: False
    :heap_only only return the whole heap. default: False
    :stack_heap return 2 values as stack, heap. default False

    This decorator ONLY cares 2 things: the amount of arguments, and the __doc__

    The args will be push to the top of  stack one by one, and the __doc__
    contains all the WhiteSpace code.

    Usage:
        @wsfunction(stack_only=True)
        def swap_dup(x, y):
            \"\"\"SLTSLS\"\"\"

        dup_swap(1,2) # => [2, 1, 1]

    See test_pyws.test_wsXpy for more cases.
    """
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


def wsmark(label: str):
    """
    This decorator will register given function to engine.PYFN_MAP
    using key `lebel`, a LABLE object or a string to initialize a new LABEL

    mark a function like:

    @wsmark("ST")
    def add(a, b):
        return a + b

    then call in WhiteSpace like:

    LLS-STL

    Where LLS is the PYFN instruction and ST is the label.

    See test_pyws.test_wsXpy for more usage.
    """
    l = LABEL(label)

    def _wsmark(func):
        PYFN_MAP[l] = func
        return func

    return _wsmark


if __name__ == '__main__':
    main()