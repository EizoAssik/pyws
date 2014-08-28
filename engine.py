# encoding=utf-8


class PYWSEngine(object):
    """
    The execute engine for PYWS
    """

    def __init__(self, ins: list):
        # instruction is a list of callable that always return None
        self.pc = 0
        self.ins = ins
        self.ins_len = len(ins)
        self.meet_end = False
        self.labels = {}
        self.stack = []
        self.call_stack = []
        self.heap = {}

    def run(self, debug=False):
        while self.has_next():
            ins = self.next()
            ins(self.stack, self.heap, self.labels, self)
            self.pc += 1

    def next(self):
        ins = self.ins[self.pc]
        return ins

    def has_next(self):
        return self.pc < self.ins_len and not self.meet_end

    def call(self, label):
        self.call_stack.append(self.pc)
        self.pc = self.labels[label]

    def ret(self):
        self.pc = self.call_stack.pop()

    def end(self):
        self.meet_end = True

