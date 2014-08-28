# encoding=utf-8
"""
All builtin operations defined in WhiteSpace
"""
import operator
import sys
from engine import PYWSEngine


class WSOperation:
    NAME = "WS"
    ARGS = 0

    def __call__(self, stack, heap, labels, engine: PYWSEngine, *args,
                 **kwargs):
        pass

    def __repr__(self):
        if self.ARGS:
            names = self.__init__.__code__.co_varnames
            return self.NAME + ' ' + ', '.join(
                map(lambda n: str(getattr(self, n)),
                    filter(lambda n: hasattr(self, n), names)))
        else:
            return self.NAME

    def __str__(self):
        return self.__str__()


class StackOperation(WSOperation):
    """
    Basic Stack Maintaining Instruction
    """
    NAME = "SOP"


class PUSH(StackOperation):
    """
    S-[Space] Number Push the number onto the stack
    """
    NAME = "PUSH"
    ARGS = 1

    def __init__(self, val):
        self.val = val

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        stack.append(self.val)


class POP(StackOperation):
    """
    S-[LF][LF] Discard the top item on the stack
    """
    NAME = "POP"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        stack.pop()


class TOP_COPY(StackOperation):
    """
    S-[LF][Space] Duplicate the top item on the stack
    """
    NAME = "TOP-COPY"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        stack.append(stack[-1])


class NTH_COPY(StackOperation):
    """
    S-[Tab][Space] Copy the nth item on the stack given by the argument
    onto the top of the stack
    """
    NAME = "NTH-COPY"
    ARGS = 1

    def __init__(self, index):
        self.index = index

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        stack.append(stack[self.index])


class STACK_SKIP(StackOperation):
    """
    S-[Tab][LF] Slide n items off the stack, keeping the top item
    """
    NAME = "STACK-SKIP"

    def __init__(self, n):
        self.n = n

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        if len(stack) - 1 > self.n:
            for _ in range(self.n):
                stack.pop(0)
        else:
            top = stack[-1]
            stack.clear()
            stack.append(top)


class TOP_SWAP(StackOperation):
    """
    S-[LF][Tab] Swap the top two items on the stack
    """
    NAME = "TOP-SWAP"

    def __call__(self, stack, heap, *args, **kwargs):
        stack[-1], stack[-2] = stack[-2], stack[-1]


class HeapOperation(WSOperation):
    """
    Basic Heap Maintaining Instruction
    """
    NAME = "HOP"


# TT
# IMP:
class STORE(HeapOperation):
    """
    TT-[Space] Store
    """
    NAME = "STORE"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        val = stack.pop()
        key = stack.pop()
        heap[key] = val


class RETRIEVE(HeapOperation):
    """
    TT-[Tab] Retrieve
    """

    NAME = "RETRIEVE"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        key = stack.pop()
        val = heap[key]
        stack.append(val)


class AlgebraOperation(WSOperation):
    """
    Basic Algebra Instruction
    """
    NAME = "Algebra"

    def __init__(self):
        self.op = operator.add

    @staticmethod
    def take_arg(stack):
        a = stack.pop()
        b = stack.pop()
        return a, b

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        val = self.op(*AlgebraOperation.take_arg(stack))
        stack.append(val)


class ADD(AlgebraOperation):
    """
    TS-[Space][Space]    Addition
    """
    NAME = "ADD"

    def __init__(self):
        super().__init__()
        self.op = operator.add


class SUB(AlgebraOperation):
    """
    TS-[Space][Tab]    Subtraction
    """
    NAME = "SUB"

    def __init__(self):
        super().__init__()
        self.op = operator.sub


class MUL(AlgebraOperation):
    """
    TS-[Space][LF]    Multiplication
    """
    NAME = "MUL"

    def __init__(self):
        super().__init__()
        self.op = operator.mul


class DIV(AlgebraOperation):
    """
    TS-[Tab][Space]    Integer Division
    """
    NAME = "DIV"

    def __init__(self):
        super().__init__()
        self.op = operator.floordiv


class MOD(AlgebraOperation):
    """
    TS-[Tab][Tab]    Modulo
    """
    NAME = "MOD"

    def __init__(self):
        super().__init__()
        self.op = operator.mod


class IOOperation(WSOperation):
    """
    Basic IO Instruction
    """
    NAME = "IO"


class PRINT_CHAR(IOOperation):
    """
    TL-[Space][Space] Output the character at the top of the stack
    """
    NAME = "PRINT-CHAR"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        sys.stdout.write(chr(stack.pop()))


class PRINT_NUM(IOOperation):
    """
    TL-[Space][Tab] Output the number at the top of the stack
    """
    NAME = "PRINT-NUM"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        sys.stdout.write(str(stack.pop()))


class READ_CHAR_TO_HEAP(IOOperation):
    """
    TL-[Tab][Space] Read a character and place it in the location
    given by the top of the stack
    """

    NAME = "READ-CHAR-TO-HEAP"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        key = stack.pop()
        s = input()
        val = int(s)
        heap[key] = val


class READ_NUM_TO_HEAP(IOOperation):
    """
    TL-[Tab][Tab] Read a number and place it in the location
    given by the top of the stack
    """

    NAME = "READ-NUM-TO-HEAP"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        key = stack.pop()
        s = input()
        val = ord(s[0])
        heap[key] = val


class FlowOperation(WSOperation):
    """
    Basic Control Flow Instruction
    Control Flow depending on the return value of __call__ method
    The execute engine use these return values to change it's
    behavior.
    """
    NAME = "CF"


class MARK(FlowOperation):
    """
    L-[Space][Space] Mark a location in the program
    """
    NAME = "MARK"
    ARGS = 1

    def __init__(self, label):
        self.label = label

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        labels[self.label] = engine.pc


class CALL(FlowOperation):
    """
    L-[Space][Tab] Call a subroutine
    """
    NAME = "CALL"
    ARGS = 1

    def __init__(self, label):
        self.label = label

    def __call__(self, stack, heap, labels, engine: PYWSEngine, *args,
                 **kwargs):
        engine.call(self.label)


class JUMP(FlowOperation):
    """
    L-[Space][LF] Jump unconditionally to a label
    """
    NAME = "JUMP"
    ARGS = 1

    def __init__(self, label):
        self.label = label

    def __call__(self, stack, heap, labels, engine: PYWSEngine, *args,
                 **kwargs):
        engine.pc = labels[self.label]


class JS(FlowOperation):
    """
    L-[Tab][Tab] Jump to a label if the top of the stack is negative
    """
    NAME = "JS"
    ARGS = 1

    def __init__(self, label):
        self.label = label

    def __call__(self, stack, heap, labels, engine: PYWSEngine, *args,
                 **kwargs):
        top = stack.pop()
        if top < 0:
            engine.pc = labels[self.label]


class JZ(FlowOperation):
    """
    L-[Tab][Space] Jump to a label if the top of the stack is zero
    """
    NAME = "JZ"
    ARGS = 1

    def __init__(self, label):
        self.label = label

    def __call__(self, stack, heap, labels, engine: PYWSEngine, *args,
                 **kwargs):
        top = stack.pop()
        if top == 0:
            engine.pc = labels[self.label]


class RETURN(FlowOperation):
    """
    L-[Tab][LF] End a subroutine and transfer control back to the caller
    """
    NAME = "RETURN"

    def __call__(self, stack, heap, labels, engine: PYWSEngine, *args,
                 **kwargs):
        engine.ret()


class END(FlowOperation):
    """
    L-[LF][LF] End the program
    """
    NAME = "END"

    def __call__(self, stack, heap, labels, engine: PYWSEngine, *args,
                 **kwargs):
        engine.end()
