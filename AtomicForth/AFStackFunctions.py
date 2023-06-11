from .AFTypes import *


def af_drop(state: ForthState):
    state.pop()


def af_dup(state: ForthState):
    state.push(state.peek())


def af_swap(state: ForthState):
    a = state.pop()
    b = state.pop()
    state.push(a)
    state.push(b)


def af_over(state: ForthState):
    state.push(state.data_stack[-2])


def af_rot(state: ForthState):
    state.push(state.pop(-3))


def af_init_stack_functions(state: ForthState):
    state.add_word("drop", af_drop)
    state.add_word("dup", af_dup)
    state.add_word("swap", af_swap)
    state.add_word("over", af_over)
    state.add_word("rot", af_rot)
