# encoding=utf-8
"""
All builtin operations defined in WhiteSpace
"""
import operator
import sys


class WSOperation:
    NAME = "WS"
    SRC = ""
    ARGS = 0

    def __call__(self, stack, heap, labels, engine, *args,
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

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.NAME != other.NAME:
            return False
        if self.ARGS != other.ARGS:
            return False
        self_names = self.__init__.__code__.co_varnames
        other_names = other.__init__.__code__.co_varnames
        if self_names != other_names:
            return False
        self_vars = [getattr(self, n) for n in self_names if hasattr(self, n)]
        other_vars = [getattr(other, n) for n in self_names if
                      hasattr(other, n)]
        if self_vars != other_vars:
            return False
        return True

    @classmethod
    def ir(cls):
        return cls.NAME


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
    SRC = "SS"
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
    SRC = "SLL"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        stack.pop()


class DUP(StackOperation):
    """
    S-[LF][Space] Duplicate the top item on the stack
    """
    NAME = "DUP"
    SRC = "SLS"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        stack.append(stack[-1])


class COPY(StackOperation):
    """
    S-[Tab][Space] Copy the nth item on the stack given by the argument
    onto the top of the stack
    """
    NAME = "COPY"
    SRC = "STS"
    ARGS = 1

    def __init__(self, index):
        self.index = index

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        stack.append(stack[self.index])


class SKIP(StackOperation):
    """
    S-[Tab][LF] Slide n items off the stack, keeping the top item
    """
    NAME = "SKIP"
    SRC = "STL"

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


class SWAP(StackOperation):
    """
    S-[LF][Tab] Swap the top two items on the stack
    """
    NAME = "SWAP"
    SRC = "SLT"

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
    SRC = "TTS"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        val = stack.pop()
        key = stack.pop()
        heap[key] = val


class RETRIEVE(HeapOperation):
    """
    TT-[Tab] Retrieve
    """

    NAME = "RETRIEVE"
    SRC = "TTT"

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
    SRC = "TSSS"

    def __init__(self):
        super().__init__()
        self.op = operator.add


class SUB(AlgebraOperation):
    """
    TS-[Space][Tab]    Subtraction
    """
    NAME = "SUB"
    SRC = "RSST"

    def __init__(self):
        super().__init__()
        self.op = operator.sub


class MUL(AlgebraOperation):
    """
    TS-[Space][LF]    Multiplication
    """
    NAME = "MUL"
    SRC = "TSSL"

    def __init__(self):
        super().__init__()
        self.op = operator.mul


class DIV(AlgebraOperation):
    """
    TS-[Tab][Space]    Integer Division
    """
    NAME = "DIV"
    SRC = "TSTS"

    def __init__(self):
        super().__init__()
        self.op = operator.floordiv


class MOD(AlgebraOperation):
    """
    TS-[Tab][Tab]    Modulo
    """
    NAME = "MOD"
    SRC = "TSTT"

    def __init__(self):
        super().__init__()
        self.op = operator.mod


class IOOperation(WSOperation):
    """
    Basic IO Instruction
    """
    NAME = "IO"


class PCHR(IOOperation):
    """
    TL-[Space][Space] Output the character at the top of the stack
    """
    NAME = "PCHR"
    SRC = "TLSS"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        sys.stdout.write(chr(stack.pop()))


class PNUM(IOOperation):
    """
    TL-[Space][Tab] Output the number at the top of the stack
    """
    NAME = "PNUM"
    SRC = "TLST"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        sys.stdout.write(str(stack.pop()))


class RCHR(IOOperation):
    """
    TL-[Tab][Space] Read a character and place it in the location
    given by the top of the stack
    """

    NAME = "RCHR"
    SRC = "TLTS"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        while len(engine.buffer) == 0:
            engine.buffer = list(input() + '\n')
        c = engine.buffer.pop(0)
        key = stack.pop()
        heap[key] = ord(c)
        if kwargs.get('debug', False):
            print('STORE', '{:03d} ({!r})'.format(ord(c), c), '->', key)


class RNUM(IOOperation):
    """
    TL-[Tab][Tab] Read a number and place it in the location
    given by the top of the stack
    """

    NAME = "RNUM"
    SRC = "TLTT"

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        s = int(input())
        key = stack.pop()
        heap[key] = s
        if kwargs.get('debug', False):
            print('STORE', s, '->', key)


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
    SRC = "LSS"
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
    SRC = "LST"
    ARGS = 1

    def __init__(self, label):
        self.label = label

    def __call__(self, stack, heap, labels, engine, *args,
                 **kwargs):
        engine.call(self.label)


class PYFN(FlowOperation):
    """
    L-[LF][Space] Call Python function
    """
    NAME = "PYFN"
    SRC = "LLS"
    ARGS = 1

    def __init__(self, label):
        self.label = label

    def __call__(self, stack, heap, labels, engine, *args, **kwargs):
        engine.foreign(self.label)


class JUMP(FlowOperation):
    """
    L-[Space][LF] Jump unconditionally to a label
    """
    NAME = "JUMP"
    SRC = "LSL"
    ARGS = 1

    def __init__(self, label):
        self.label = label

    def __call__(self, stack, heap, labels, engine, *args,
                 **kwargs):
        engine.pc = labels[self.label]


class JS(FlowOperation):
    """
    L-[Tab][Tab] Jump to a label if the top of the stack is negative
    """
    NAME = "JS"
    SRC = "LTT"
    ARGS = 1

    def __init__(self, label):
        self.label = label

    def __call__(self, stack, heap, labels, engine, *args,
                 **kwargs):
        top = stack.pop()
        if top < 0:
            engine.pc = labels[self.label]


class JZ(FlowOperation):
    """
    L-[Tab][Space] Jump to a label if the top of the stack is zero
    """
    NAME = "JZ"
    SRC = "LTS"
    ARGS = 1

    def __init__(self, label):
        self.label = label

    def __call__(self, stack, heap, labels, engine, *args,
                 **kwargs):
        top = stack.pop()
        if top == 0:
            engine.pc = labels[self.label]


class RET(FlowOperation):
    """
    L-[Tab][LF] End a subroutine and transfer control back to the caller
    """
    NAME = "RET"
    SRC = "LTL"

    def __call__(self, stack, heap, labels, engine, *args,
                 **kwargs):
        engine.ret()


class END(FlowOperation):
    """
    L-[LF][LF] End the program
    """
    NAME = "END"
    SRC = "LLL"

    def __call__(self, stack, heap, labels, engine, *args,
                 **kwargs):
        engine.end()


class WSLiteral(object):
    NAME = "LITERAL"

    def __init__(self, literal: str):
        if isinstance(literal, str):
            self.literal = literal.translate({ord('S'): '0', ord('T'): '1'})
            self.val = self.eval_literal()
        elif isinstance(literal, WSLiteral):
            self.val = literal.val
            self.literal = literal.literal
        elif isinstance(literal, int):
            self.literal = bin(literal)[2:]
            self.val = literal
        else:
            raise TypeError('Cannot convert \'{}\' to {}'
                            .format(repr(literal), self.NAME))

    def __hash__(self):
        return hash(self.val)

    def __eq__(self, other):
        if isinstance(other, int) and other == self.val:
            return True
        if type(self) != type(other):
            return False
        if self.val != other.val:
            return False
        return True

    def __repr__(self):
        return str(self.val)

    def __str__(self):
        return self.__repr__()

    def eval_literal(self):
        return int(self.literal, base=2)

    def ir(self):
        pass


class LABEL(WSLiteral):
    NAME = "LABEL"

    def ir(self):
        return '0' + str(self.val)


class NUMBER(WSLiteral):
    NAME = "NUMBER"

    def eval_literal(self):
        negative = self.literal[0] == '1'
        val = self.literal[1:]
        if negative:
            val = val.translate({ord('0'): '1', ord('1'): '0'})
        return (-1 if negative else 1) * int(val, base=2)

    def __int__(self):
        return self.val

    def __float__(self):
        return float(self.val)

    def __add__(self, other):
        return other.__add__(self.val)

    def __sub__(self, other):
        return other.__sub__(self.val)

    def __mul__(self, other):
        return other.__mul__(self.val)

    def __truediv__(self, other):
        return other.__truediv__(self.val)

    def __floordiv__(self, other):
        return other.__floordiv__(self.val)

    def __mod__(self, other):
        return other.__mod__(self.val)

    def __radd__(self, other):
        return other.__add__(self.val)

    def __rsub__(self, other):
        return other.__sub__(self.val)

    def __rmul__(self, other):
        return other.__mul__(self.val)

    def __rtruediv__(self, other):
        return other.__truediv__(self.val)

    def __rfloordiv__(self, other):
        return other.__floordiv__(self.val)

    def __rmod__(self, other):
        return other.__mod__(self.val)

    def ir(self):
        if self.val < 0:
            return str(self.val)
        return '0{}'.format(self.val)

