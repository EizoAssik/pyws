# encoding=utf-8
from wsbuiltin import PUSH, NTH_COPY, TOP_SWAP, POP, TOP_COPY, STACK_SKIP
from wsbuiltin import RETRIEVE, STORE
from wsbuiltin import ADD, SUB, MUL, DIV, MOD
from wsbuiltin import MARK, CALL, JUMP, JS, JZ, RETURN, END
from wsbuiltin import PRINT_NUM, PRINT_CHAR, READ_CHAR_TO_HEAP, READ_NUM_TO_HEAP
from wsbuiltin import NUMBER, LABEL


# Stack Operation
# IMP: [Space]
# Command       Parameters  Meaning
# [Space]         Number    Push the number onto the stack
# [LF][Space]       -       Duplicate the top item on the stack
# [Tab][Space]    Number    Copy the nth item on the stack given by the argument
#                           onto the top of the stack
# [LF][Tab]         -       Swap the top two items on the stack
# [LF][LF]          -       Discard the top item on the stack
# [Tab][LF]       Number    Slide n items off the stack, keeping the top item

SOP = {
    "S": [None, (PUSH, 1, NUMBER)],
    "T": [
        {
            "S": (NTH_COPY, 1, NUMBER),
            "L": (STACK_SKIP, 1, NUMBER)
        },
        None],
    "L": [
        {
            "S": (TOP_COPY, 0, None),
            "T": (TOP_SWAP, 0, None),
            "L": (POP, 0, None)
        },
        None]
}


# Heap Operation
# IMP:
# Command     Meaning
# [Space]     Store
# [Tab]       Retrieve

HOP = {"S": [None, (STORE, 0, None)],
       "T": [None, (RETRIEVE, 0, None)],
       "L": [None, None]}

# Arithmetic Operation
# IMP: [Tab][Space]
# Command          Meaning
# [Space][Space]   Addition
# [Space][Tab]     Subtraction
# [Space][LF]      Multiplication
# [Tab][Space]     Integer Division
# [Tab][Tab]       Modulo

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
# Command        Parameters  Meaning
# [Space][Space]   Label     Mark a location in the program
# [Space][Tab]     Label     Call a subroutine
# [Space][LF]      Label     Jump unconditionally to a label
# [Tab][Space]     Label     Jump to a label if the top of the stack is zero
# [Tab][Tab]       Label     Jump to a label if the top of the stack is negative
# [Tab][LF]          -       End a subroutine and transfer control back to the
# caller
# [LF][LF]           -       End the program

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
            "L": (RETURN, 0, None),
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
# Command          Meaning
# [Space][Space]   Output the character at the top of the stack
# [Space][Tab]     Output the number at the top of the stack
# [Tab][Space]     Read a character and place it in the location
#                  given by the top of the stack
# [Tab][Tab]       Read a number and place it in the location
#                  given by the top of the stack

IO = {
    "S": [
        {
            "S": (PRINT_CHAR, 0, None),
            "T": (PRINT_NUM, 0, None),
        },
        None],
    "T": [
        {
            "S": (READ_CHAR_TO_HEAP, 0, None),
            "T": (READ_NUM_TO_HEAP, 0, None),
        },
        None],
    "L": [None, None]
}

IMP = {
    "S": [None, SOP],
    "T": [{"S": [AR, None], "T": [HOP, None], "L": [IO, None]}, None],
    "L": [None, FC]
}

