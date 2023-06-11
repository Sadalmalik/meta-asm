from .AFTypes import *


def af_get_var(state: ForthState):
    a_name: ForthAtom = state.pop()
    if a_name.type != AtomType.SYMBOL:
        raise Exception(f"Wrong key type! Expect SYMBOL, but found: {a_name.type}")
    if a_name.data not in state.context:
        raise Exception(f"'{a_name.data}' not found in context!")
    state.push(state.context[a_name.data])


def af_set_var(state: ForthState):
    a_name: ForthAtom = state.pop()
    a_value: ForthAtom = state.pop()
    if a_name.type != AtomType.SYMBOL:
        raise Exception(f"Wrong key type! Expect SYMBOL, but found: {a_name.type}")
    state.context[a_name.data] = a_value


def af_init_variable_functions(state: ForthState):
    state.add_word("GET", af_get_var)
    state.add_word("SET", af_set_var)
