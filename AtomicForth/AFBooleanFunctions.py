from .AFTypes import *


def internal_get_bool(state: ForthState) -> bool:
    a = state.pop()
    if a.type != AtomType.BOOL:
        raise Exception("Expect bool on stack!")
    return a.data


def af_bool_not(state: ForthState):
    a = internal_get_bool(state)
    state.push(ForthAtom(type=AtomType.BOOL, data=not a))


def af_bool_and(state: ForthState):
    a = internal_get_bool(state)
    b = internal_get_bool(state)
    state.push(ForthAtom(type=AtomType.BOOL, data=a and b))


def af_bool_or(state: ForthState):
    a = internal_get_bool(state)
    b = internal_get_bool(state)
    state.push(ForthAtom(type=AtomType.BOOL, data=a or b))


def af_bool_xor(state: ForthState):
    a = internal_get_bool(state)
    b = internal_get_bool(state)
    state.push(ForthAtom(type=AtomType.BOOL, data=a ^ b))


def af_init_bool_functions(state: ForthState):
    state.add_word("not", af_bool_not)
    state.add_word("and", af_bool_and)
    state.add_word("or", af_bool_or)
    state.add_word("xor", af_bool_xor)