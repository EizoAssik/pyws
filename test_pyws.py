# from lexer import Lexer
import style
from wsbuiltin import ADD, PUSH, SUB
import wsbuiltin
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


def test_literal():
    assert "<NUMBER 1001/-6>" == repr(wsbuiltin.NUMBER('TSST'))
    assert "<NUMBER 01011/11>" == repr(wsbuiltin.NUMBER('STSTT'))
    assert "<LABEL 1001/9>" == repr(wsbuiltin.LABEL('TSST'))
    assert 3 == wsbuiltin.NUMBER("ST") + 2
    assert 0 == 1 - wsbuiltin.NUMBER("ST")
    assert 6 == wsbuiltin.NUMBER("STT") * wsbuiltin.NUMBER("STS")
    assert 2 == 5 // wsbuiltin.NUMBER("STS")
    assert 9 == 10 + wsbuiltin.NUMBER("TS")
    assert 1 == 3 % wsbuiltin.NUMBER("STS")
