# from lexer import Lexer
import style
from wsbuiltin import ADD, PUSH, SUB, NUMBER, LABEL
from wslexer import Reader
from pyws import compiler, disassembler, assembler
from engine import PYWSEngine


def test_source():
    assert 'SS' == ''.join(Reader('a s ', style.ORIGIN).code)
    assert 'LS' == ''.join(Reader('aLsS').code)


def test_iter():
    assert 'SS' == ''.join(Reader('a s ', style.ORIGIN).__iter__())
    assert 'LS' == ''.join(Reader('aLsS').__iter__())


def test_compiler():
    assert [ADD()] == compiler('TSSS')
    assert [ADD(), SUB()] == compiler('TSSSTSST')
    assert [PUSH(NUMBER('STS'))] == compiler('SSSTSL')


def test_repr():
    assert "PUSH <NUMBER 011/3>" == repr(PUSH(NUMBER('STT')))


def test_disassembler():
    assert "ADDSUB" == disassembler(compiler("TSSSTSST"))
    assert "ADD-SUB" == disassembler(compiler("TSSSTSST"), sep='-')


def test_literal():
    assert "<NUMBER 1001/-6>" == repr(NUMBER('TSST'))
    assert "<NUMBER 01011/11>" == repr(NUMBER('STSTT'))
    assert "<LABEL 1001/9>" == repr(LABEL('TSST'))
    assert 3 == NUMBER("ST") + 2
    assert 0 == 1 - NUMBER("ST")
    assert 6 == NUMBER("STT") * NUMBER("STS")
    assert 2 == 5 // NUMBER("STS")
    assert 9 == 10 + NUMBER("TS")
    assert 1 == 3 % NUMBER("STS")
    assert hash(NUMBER("STS")) == hash(NUMBER("STS"))
    assert NUMBER("STSS") == NUMBER("STSS")
    assert NUMBER("SSTS") == NUMBER("STS")


def test_assembler():
    assert "SS;STSTSL" == assembler("PUSH 10")

def ws_run(src: str) -> ([], {}):
    return PYWSEngine(compiler(src)).run()

def test_engine():
    # PUSH 01 ; PUSH 03 ; ADD
    assert ([4], {}) == ws_run("SSSTL;SSSTTL;TSSS")
    # PUSH 01 ; PUSH 02 ; STORE
    assert ([], {NUMBER("ST"): NUMBER("STS")}) == ws_run("SSSTL;SSSTSL;TTS")
    # PUSH 03 ; PUSH 01 ; STORE ; PUSH 03 ; RETRIEVE
    assert ([NUMBER("ST")], {NUMBER("STT"): NUMBER("ST")}) == ws_run("SSSTTL;SSSTL;TTS;SSSTTL;TTT")
    # PUSH 01 ; TOP-COPY ; STORE ;
    assert ([NUMBER("STTSS")], {}) ==  ws_run('SS;STL;SS;STSL;TSSS;SLL;SS;STTL;SS;STSSL;TSSL')
