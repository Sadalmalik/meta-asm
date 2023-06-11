# Root of Atomic Forth
import sys

from .AFTypes import *
from .AFExecution import *
from .AFGeneral import *
from .AFStackFunctions import *
from .AFVariablesFunctions import *
from .AFMathFunctions import *
from .AFBooleanFunctions import *
from .AFInput import *
from .ByteBuilder import *


def af_build():
    state = ForthState()

    af_init_execution_functions(state)
    af_init_general_functions(state)
    af_init_stack_functions(state)
    af_init_math_functions(state)
    af_init_bool_functions(state)
    af_init_variable_functions(state)
    af_init_input_functions(state)

    return state


def run_forth(file=None):
    state = af_build()
    if file is None:
        state.stream_stack.append(sys.stdin)
    else:
        state.push(ForthAtom(AtomType.STRING, file))
        af_include(state)
    af_eval(state)
