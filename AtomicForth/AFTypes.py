from enum import Enum
from dataclasses import dataclass


class ForthMode(Enum):
    EXIT = 0
    EXECUTE = 1
    COMPILE = 2


class AtomType(Enum):
    UNDEFINED = 0
    NATIVE = 1
    WORD = 2
    SYMBOL = 3
    BOOL = 4
    CHAR = 5
    INTEGER = 6
    FLOAT = 7
    STRING = 8


class ForthAtom:
    def __init__(self, type: AtomType, data: object):
        self.type = type
        self.data = data

    def __str__(self):
        return f"( {self.type} , {self.data} )"


@dataclass
class ForthState:
    pointer = -1
    context = dict()
    code_block = list()
    data_stack = list()
    call_stack = list()
    mode = ForthMode.EXECUTE
    word = None  # ForthAtom
    stream_stack = list()
    include_stack = list()

    def push(self, atom: ForthAtom):
        self.data_stack.append(atom)

    def peek(self):
        return self.data_stack[-1]

    def pop(self, index=-1):
        return self.data_stack.pop(index)

    def add_word(self, name, call, immediate=False):
        self.context[name] = ForthAtom(AtomType.NATIVE, (immediate, call))

    def eval_file(self, path):
        pass


ATOM_NEXT = ForthAtom(AtomType.SYMBOL, 'next')
ATOM_EXIT = ForthAtom(AtomType.SYMBOL, 'exit')
ATOM_RET = ForthAtom(AtomType.SYMBOL, 'ret')
