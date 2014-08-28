# encoding=utf-8
from wsbuiltin import PUSH, COPY, SWAP, POP, DUP, SKIP
from wsbuiltin import RETRIEVE, STORE
from wsbuiltin import ADD, SUB, MUL, DIV, MOD
from wsbuiltin import MARK, CALL, JUMP, JS, JZ, RET, END
from wsbuiltin import PNUM, PCHR, RCHR, RNUM
from wsbuiltin import NUMBER, LABEL


# Stack Operation
# IMP: [Space]
# Command      Name Parameters Meaning
# [Space]      PUSH   Number   Push the number onto the stack
# [LF][Space]  DUP      -      Duplicate the top item on the stack
# [Tab][Space] COPY   Number   Copy the nth item on the stack given by the
#                              argument onto the top of the stack
# [LF][Tab]    SWAP     -      Swap the top two items on the stack
# [LF][LF]     POP      -      Discard the top item on the stack
# [Tab][LF]    SKIP   Number   Slide n items off the stack, keeping the top item

SOP = {
    "S": [None, (PUSH, 1, NUMBER)],
    "T": [
        {
            "S": (COPY, 1, NUMBER),
            "L": (SKIP, 1, NUMBER)
        },
        None],
    "L": [
        {
            "S": (DUP, 0, None),
            "T": (SWAP, 0, None),
            "L": (POP, 0, None)
        },
        None]
}


# Heap Operation
# IMP: [Tab][Tab]
# Command NAME     Meaning
# [Space] STORE    Store
# [Tab]   RETRIEVE Retrieve

HOP = {"S": [None, (STORE, 0, None)],
       "T": [None, (RETRIEVE, 0, None)],
       "L": [None, None]}

# Arithmetic Operation
# IMP: [Tab][Space]
# Command        NAME Meaning
# [Space][Space] ADD  Addition
# [Space][Tab]   SUB  Subtraction
# [Space][LF]    MUL  Multiplication
# [Tab][Space]   DIV  Integer Division
# [Tab][Tab]     MOD  Modulo

AR = {
    "S": [
        {
            "S": (ADD, 0, None),
            "T": (SUB, 0, None),
            "L": (MUL, 0, None),
        },
        None],
    "T": [
        {
            "S": (DIV, 0, None),
            "T": (MOD, 0, None),
        },
        None],
    "L": [None, None]}

# Control Flow
# IMP: [LF]
# Command        NAME Parameters Meaning
# [Space][Space] MARK  Label     Mark a location in the program
# [Space][Tab]   CALL  Label     Call a subroutine
# [Space][LF]    JUMP  Label     Jump unconditionally to a label
# [Tab][Space]   JZ    Label     Jump to a label if the top of the stack is zero
# [Tab][Tab]     JS    Label     Jump to a label if the top of the stack is
#                                negative
# [Tab][LF]      RET     -       End a subroutine and transfer control back to
#                                the caller
# [LF][LF]       END     -       End the program

FC = {
    "S": [
        {
            "S": (MARK, 1, LABEL),
            "T": (CALL, 1, LABEL),
            "L": (JUMP, 1, LABEL),
        },
        None],
    "T": [
        {
            "S": (JZ, 1, LABEL),
            "T": (JS, 1, LABEL),
            "L": (RET, 0, None),
        },
        None],
    "L": [
        {
            "L": (END, 0, None)
        },
        None]
}

# IO
# IMP: [Tab][LF]
# Command        NAME  Meaning
# [Space][Space] PCHR  Output the character at the top of the stack
# [Space][Tab]   PNUM  Output the number at the top of the stack
# [Tab][Space]   RCHR  Read a character and place it in the location
#                      given by the top of the stack
# [Tab][Tab]     RNUM  Read a number and place it in the location
#                      given by the top of the stack

IO = {
    "S": [
        {
            "S": (PCHR, 0, None),
            "T": (PNUM, 0, None),
        },
        None],
    "T": [
        {
            "S": (RCHR, 0, None),
            "T": (RNUM, 0, None),
        },
        None],
    "L": [None, None]
}

# IMP
# [Space]      SOP
# [Tab][Tab]   HOP
# [Tab][Space] Arithmetic
# [Tab][LF]    IO
# [LF]         Control Flow

IMP = {
    "S": [None, SOP],
    "T": [{"S": [AR, None], "T": [HOP, None], "L": [IO, None]}, None],
    "L": [None, FC]
}
