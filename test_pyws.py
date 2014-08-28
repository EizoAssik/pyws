# from lexer import Lexer
import style
from wsbuiltin import ADD, PUSH, SUB
from wslexer import Reader
from pyws import wscompiler, disassembler


def test_source():
    assert 'SS' == ''.join(Reader('a s ', style.ORIGIN).code)
    assert 'LS' == ''.join(Reader('aLsS').code)


def test_iter():
    assert 'SS' == ''.join(Reader('a s ', style.ORIGIN).__iter__())
    assert 'LS' == ''.join(Reader('aLsS').__iter__())


def test_compiler():
    assert [ADD()] == wscompiler('TSSS')
    assert [ADD(), SUB()] == wscompiler('TSSSTSST')


def test_repr():
    assert "PUSH 3" == repr(PUSH(3))


def test_disassembler():
    assert "ADDSUB" == disassembler(wscompiler("TSSSTSST"))
    assert "ADD-SUB" == disassembler(wscompiler("TSSSTSST"), sep='-')


if __name__ == '__main__':
    test_compiler()