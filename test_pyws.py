# from lexer import Lexer
import style
from wsbuiltin import ADD, PUSH, SUB, NUMBER, LABEL
from wslexer import Reader
from pyws import op_compiler, disassembler, assembler, wsfunction, wsmark, \
    ir_compiler
from engine import PYWSEngine


def test_source():
    assert 'SS' == ''.join(Reader('a s ', style.ORIGIN).code)
    assert 'LS' == ''.join(Reader('aLsS').code)


def test_iter():
    assert 'SS' == ''.join(Reader('a s ', style.ORIGIN).__iter__())
    assert 'LS' == ''.join(Reader('aLsS').__iter__())


def test_compiler():
    assert [ADD()] == op_compiler('TSSS')
    assert [ADD(), SUB()] == op_compiler('TSSSTSST')
    assert [PUSH(NUMBER('STS'))] == op_compiler('SSSTSL')


def test_ir_compiler():
    assert "ADD" == ir_compiler("TSSS")
    assert "PUSH 01\nPUSH 03\nADD" == ir_compiler("SSSTL;SSSTTL;TSSS")


def test_repr():
    assert "PUSH 3" == repr(PUSH(NUMBER('STT')))


def test_disassembler():
    assert "ADDSUB" == disassembler(op_compiler("TSSSTSST"))
    assert "ADD-SUB" == disassembler(op_compiler("TSSSTSST"), sep='-')
    assert "PUSH -10;DUP" == disassembler(op_compiler("SSTSTSTLSLS"), sep=';')


def test_literal():
    assert "-6" == repr(NUMBER('TSST'))
    assert "11" == repr(NUMBER('STSTT'))
    assert "9" == repr(LABEL('TSST'))
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
    assert "SS;STSTSL" == assembler("PUSH 10")[0]
    assert "SS;SSL;SS;STL" == assembler("PUSHS [0,1]")[0]


def ws_run(src: str, style=style.STL) -> ([], {}):
    return PYWSEngine(op_compiler(src, style=style)).run()


def test_engine():
    # PUSH 01 ; PUSH 03 ; ADD
    assert ([4], {}) == ws_run("SSSTL;SSSTTL;TSSS")
    # PUSH 01 ; PUSH 02 ; STORE
    assert ([], {NUMBER("ST"): NUMBER("STS")}) == ws_run("SS;STL;SS;STSL;TTS")
    # PUSH 03 ; PUSH 01 ; STORE ; PUSH 03 ; RETRIEVE
    assert ([NUMBER("ST")], {NUMBER("STT"): NUMBER("ST")}) == ws_run(
        "SSSTTL;SSSTL;TTS;SSSTTL;TTT")
    # PUSH 01 ; TOP-COPY ; STORE ;
    # PUSH 01 ; PUSH 02 ; ADD ; POP ; PUSH 03 ; PUSH 04 ; MUL
    assert ([NUMBER("STTSS")], {}) == ws_run(
        'SS;STL;SS;STSL;TSSS;SLL;SS;STTL;SS;STSSL;TSSL')


@wsfunction()
def add(a, b):
    """TSSS"""


@wsmark("TT")
@wsfunction()
def wsadd(a, b):
    """TSSS"""


@wsmark("ST")
def mul(a, b):
    return a * b


def test_wsXpy():
    assert 3 == add(1, 2)
    # PUSH 03 ; PUSH 02 ; PYFN 01
    assert 6 == ws_run("SSSTTL;SSSTSL;LLSSTL")[0].pop()
    # PUSH 03 ; PUSH 02 ; PYFN -1
    assert 5 == ws_run("SSSTTL;SSSTSL;LLSTTL")[0].pop()
