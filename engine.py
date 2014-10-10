# encoding=utf-8
from wsbuiltin import MARK, LABEL, NUMBER
import copy

# This records `foreign` (for WhiteSpace) functions
# See pyws.wsmark & PYWSEngine.foreign for more information
PYFN_MAP = {}


class PYWSEngine(object):
    """
    The execute engine for PYWS.
    """

    def __init__(self, ins, stack=None, heap=None):
        # instruction is a list of callable that always return None
        self.pc = 0
        self.ins = ins
        self.ins_len = len(ins)
        self.meet_end = False
        self.labels = {}
        self.history = []
        self.buffer = []
        if stack:
            self.stack = list(stack)
        else:
            self.stack = []
        if heap:
            self.heap = heap
        else:
            self.heap = {}
        self.heap = {}
        self.call_stack = []
        for i, ins in enumerate(self.ins):
            if isinstance(ins, MARK):
                self.labels[ins.label] = i

    def run(self, debug=False, traceall=False):
        """
        If debug is True, log history after every operation
        """
        if traceall:
            self.append_history(self.pc, None, self.stack, self.heap)
        try:
            while self.has_next():
                ins = self.next()
                ins(self.stack, self.heap, self.labels, self, debug=debug)
                if traceall:
                    self.append_history(self.pc, None, self.stack, self.heap)
                self.pc += 1
        except KeyboardInterrupt:
            pass
        return self.stack, self.heap

    def append_history(self, pc, ins, stack, heap):
        self.history.append((pc,
                             ins,
                             copy.deepcopy(stack),
                             copy.deepcopy(heap)))

    def next(self):
        """
        get next instruction by self.pc
        """
        ins = self.ins[self.pc]
        return ins

    def has_next(self):
        """
        Both pc out of len(ins) and call engine.end method will stop the loop
        """
        return self.pc < self.ins_len and not self.meet_end

    def call(self, label):
        """
        when meet CALL, store current pc for RET
        """
        self.call_stack.append(self.pc)
        self.pc = self.labels[label]

    def foreign(self, label):
        """
        this support foreign call for wspy.

        """
        fn = PYFN_MAP.get(label, None)
        if fn:
            argcount = fn.__code__.co_argcount
            self.stack, args = self.stack[:-argcount], self.stack[-argcount:]
            retval = fn(*args)
            if isinstance(retval, (LABEL, NUMBER, int)):
                self.stack.append(retval)
            else:
                raise TypeError

    def ret(self):
        """
        If any, reset the pc to latest CALL.
        """
        if self.call_stack:
            self.pc = self.call_stack.pop()

    def end(self):
        self.meet_end = True

