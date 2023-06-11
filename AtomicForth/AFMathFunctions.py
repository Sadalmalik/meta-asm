from .AFTypes import *


def internal_get_numbers(state: ForthState):
    b, a = state.pop(), state.pop()
    if a.type != AtomType.INTEGER and \
            a.type != AtomType.FLOAT and \
            b.type != AtomType.INTEGER and \
            b.type != AtomType.FLOAT:
        raise Exception("Expect two numbers on stack!")
    end_type = AtomType.INTEGER
    if a.type == AtomType.FLOAT or b.type == AtomType.FLOAT:
        end_type = AtomType.FLOAT
    return a.data, b.data, end_type


def af_math_add(state: ForthState):
    a, b, end_type = internal_get_numbers(state)
    state.push(ForthAtom(type=end_type, data=a + b))


def af_math_sub(state: ForthState):
    a, b, end_type = internal_get_numbers(state)
    state.push(ForthAtom(type=end_type, data=a - b))


def af_math_mul(state: ForthState):
    a, b, end_type = internal_get_numbers(state)
    state.push(ForthAtom(type=end_type, data=a * b))


def af_math_div(state: ForthState):
    a, b, end_type = internal_get_numbers(state)
    state.push(ForthAtom(type=end_type, data=a / b))


def af_math_mod(state: ForthState):
    a, b, end_type = internal_get_numbers(state)
    state.push(ForthAtom(type=end_type, data=a % b))


def safe_apply(func, *args):
    try:
        return func(*args)
    except:
        return None


def internal_parse_number(raw: str):
    if raw.startswith("0x"):
        val = safe_apply(int, raw, 16)
        if val is not None:
            return AtomType.INTEGER, val
    elif raw.startswith("0b"):
        val = safe_apply(int, raw, 2)
        if val is not None:
            return AtomType.INTEGER, val
    elif raw.isdigit():
        val = safe_apply(int, raw, 10)
        if val is not None:
            return AtomType.INTEGER, val
    else:
        val = safe_apply(float, raw)
        if val is not None:
            return AtomType.FLOAT, val
    return AtomType.UNDEFINED, None


def af_parse_number(state: ForthState):
    atom = state.pop()
    if atom.type == AtomType.SYMBOL or atom.type == AtomType.STRING:
        a_type, value = internal_parse_number(atom.data)
        if a_type == AtomType.UNDEFINED:
            state.push(ForthAtom(AtomType.BOOL, False))
        else:
            state.push(ForthAtom(a_type, value))
    else:
        raise Exception("Number parsing expects string or symbol!")


def af_init_math_functions(state: ForthState):
    state.add_word("+", af_math_add)
    state.add_word("-", af_math_sub)
    state.add_word("*", af_math_mul)
    state.add_word("/", af_math_div)
    state.add_word("%", af_math_mod)
    state.add_word("parse_number", af_parse_number)