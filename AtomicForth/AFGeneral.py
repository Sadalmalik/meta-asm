from .AFTypes import *


def af_equal(state: ForthState):
    b: ForthAtom = state.pop()
    a: ForthAtom = state.pop()
    return b.type == a.type and b.data == a.data


def af_print(state: ForthState):
    atom = state.pop()
    print(atom.data)


def af_exit(state: ForthState):
    state.mode = ForthMode.EXIT


def af_init_general_functions(state: ForthState):
    state.add_word("=", af_equal)
    state.add_word("print", af_print)
    state.add_word(ATOM_EXIT.data, af_exit)
