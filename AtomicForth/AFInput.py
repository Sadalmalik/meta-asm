import sys
import os

from .AFMathFunctions import *
from .AFTypes import *


def af_next(state: ForthState):
    # Buildin parser
    stream = state.stream_stack[-1]
    token = ''

    ch = stream.read(1)
    is_string = False
    if ch != '':
        # skip whitespaces
        while ch != '' and ch in ' \n\t':
            ch = stream.read(1)
        if ch == '"':
            is_string = True
            while True:
                ch = stream.read(1)
                if ch == '\\':
                    ch = stream.read(1)
                elif ch == '"':
                    break
                token += ch
        else:
            # read word
            while ch != '' and ch not in ' \n\t':
                token += ch
                ch = stream.read(1)
    if token == '':
        state.stream_stack.pop()
        if len(state.stream_stack) == 0:
            state.push(ATOM_EXIT)
        else:
            af_next(state)
        return
    a_type, value = internal_parse_number(token)
    if a_type != AtomType.UNDEFINED:
        state.push(ForthAtom(a_type, value))
    else:
        state.push(ForthAtom(AtomType.STRING if is_string else AtomType.SYMBOL, token))


def af_get_char(state: ForthState):
    stream = state.stream_stack[-1]
    ch = stream.read(1)
    if ch == '':
        state.push(ForthAtom(AtomType.BOOL, False))
        state.stream_stack.pop()
        if len(state.include_stack) > 0:
            state.include_stack.pop()
    else:
        state.push(ForthAtom(AtomType.STRING, ch))


def af_include(state: ForthState):
    atom: ForthAtom = state.pop()
    if atom.type != AtomType.STRING and atom.type != AtomType.SYMBOL:
        raise Exception("Expect string or symbol for filename!")
    file = str(atom.data)
    if len(state.include_stack) > 0:
        base_path = state.include_stack[-1]
        file = os.path.join(base_path, file)
        file = os.path.abspath(file)
    else:
        file = os.path.abspath(file)
    state.stream_stack.append(open(file, 'r', encoding='utf8'))
    state.include_stack.append(os.path.dirname(file))


def af_init_input_functions(state: ForthState):
    state.add_word(ATOM_NEXT.data, af_next, True)
    state.add_word("getch", af_get_char)
    state.add_word("include", af_include)
