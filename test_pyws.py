# from lexer import Lexer
import style
from wsbuiltin import ADD, PUSH
from wslexer import Lexer
from pyws import wscompiler


def test_source():
    assert 'SS' == ''.join(Lexer('a s ', style.ORIGIN).code)
    assert 'LS' == ''.join(Lexer('aLsS').code)


def test_iter():
    assert 'SS' == ''.join(Lexer('a s ', style.ORIGIN).__iter__())
    assert 'LS' == ''.join(Lexer('aLsS').__iter__())


def test_compiler():
    assert [ADD] == wscompiler('TSSS')


def test_repr():
    assert "PUSH 3" == repr(PUSH(3))
