from .AFTypes import *


def af_eval(state: ForthState):
    while state.mode != ForthMode.EXIT:
        if state.pointer != -1:
            af_eval_atom(state, state.code_block[state.pointer])
            if state.pointer > -1:
                state.pointer += 1
        else:
            # Get next atom
            af_eval_atom(state, ATOM_NEXT)
            # Execute atom
            atom = state.pop()
            af_eval_atom(state, atom)


def af_eval_atom(state: ForthState, atom: ForthAtom):
    if atom.type == AtomType.SYMBOL:
        if atom.data not in state.context:
            raise Exception(f"'{atom.data}' not found in context!")
        func = state.context[atom.data]
        immediate, code = func.data
        if immediate or state.mode != ForthMode.COMPILE:
            if func.type == AtomType.NATIVE:
                # print(f"call {code.__name__}")
                code(state)
            elif func.type == AtomType.WORD:
                state.call_stack.append(state.pointer)
                state.pointer = code
                # print(f"Enter code: {state.pointer}")
            return
    if state.mode == ForthMode.COMPILE:
        state.code_block.append(atom)
    else:
        state.push(atom)


def af_compile_atom(state: ForthState):
    atom = state.pop()
    state.code_block.append(atom)


def af_begin_word(state: ForthState):
    if state.mode == ForthMode.COMPILE:
        raise Exception("Word : not allowed during compilation!")
    af_eval_atom(state, ATOM_NEXT)
    atom = state.pop()
    if atom.type != AtomType.SYMBOL:
        raise Exception("Word name must be symbol!")
    state.mode = ForthMode.COMPILE
    state.word = ForthAtom(AtomType.WORD, (False, len(state.code_block)))
    state.context[atom.data] = state.word


def af_end_word(state: ForthState):
    state.code_block.append(ATOM_RET)
    state.mode = ForthMode.EXECUTE
    state.word = None


def af_ret(state: ForthState):
    state.pointer = state.call_stack.pop()


def af_here(state: ForthState):
    state.push(ForthAtom(AtomType.INTEGER, state.pointer))


def af_immediate(state: ForthState):
    if state.word is None:
        raise Exception("Immediate can be called only inside word definition!")
    state.word.data[0] = True


def af_branch(state: ForthState):
    state.pointer += 1
    atom = state.code_block[state.pointer]
    if atom.type != AtomType.INTEGER:
        raise Exception("Branch expects number after it!")
    state.pointer = int(atom.data)


def af_branch_cond(state: ForthState):
    state.pointer += 1
    atom: ForthAtom = state.code_block[state.pointer]
    if atom.type != AtomType.INTEGER:
        raise Exception("Branch expects number after it!")
    cond: ForthAtom = state.pop()
    if cond.type != AtomType.BOOL:
        raise Exception("Branch expects boolean on stack!")
    if cond.data is True:
        state.pointer = int(atom.data)


def af_init_execution_functions(state: ForthState):
    state.add_word(":", af_begin_word, True)
    state.add_word(";", af_end_word, True)
    state.add_word("immediate", af_immediate, True)
    state.add_word("compile", af_compile_atom)
    state.add_word(ATOM_RET.data, af_ret)
    state.add_word("here", af_here)
    state.add_word("branch", af_branch)
    state.add_word("branch?", af_branch_cond)
