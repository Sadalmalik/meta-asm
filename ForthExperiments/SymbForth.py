# Итак, главная идея проста - форт с символами как в лиспе.
#
# Важный момент - простота интерпретации.
# Почитав всякое про оригинальный форт я увидел что там, под капотом
# форт может иметь несколько вариация работы одних и тех же команд.
# Мне это не подходит!
#
# Поэтому я предварительно сформулировал в голове такой образ:
# Интерпретатор содержит в себе два предзаданных слова,
# определенных прямо на форте:
#   - Получение следующего символа из входного потока
#   - Обработка символа
#
# Ядро имеет только один режим - интерпретация.
# Ядро содержит систему контекстов.
# .
from dataclasses import dataclass

from ForthExperiments.SFContext import Context
from ForthExperiments.SFSafeIterator import SafeIterator


@dataclass
class ForthRecord:
    name: str
    immediate: bool
    isNative: bool
    content: object


class SymbForth:
    def __init__(self):
        self.stack = []
        self.eval_stack = []
        self.context = Context()
        self.mode = "INTERPRET"  # "EXECUTE", "COMPILE", "OTHER"
        self._current_word: ForthRecord = None

        # Stack words
        self._add_func( 'PUSH', self._push, False)
        self._add_func( 'DROP', self._drop, False)
        self._add_func(  'DUP', self._dup,  False)
        self._add_func( 'OVER', self._over, False)
        self._add_func( 'SWAP', self._swap, False)
        self._add_func(  'ROT', self._rot,  False)

        # Definition words
        self._add_func( ':', self._begin_word, False)
        self._add_func( ';', self._end_word, True)
        self._add_func( 'IMMEDIATE', self._set_immediate, True)

        # Math wodrs
        self._add_func( '+', self._math_sum, False)
        self._add_func( '-', self._math_sub, False)
        self._add_func( '*', self._math_mul, False)
        self._add_func( '/', self._math_div, False)
        self._add_func( '%', self._math_mod, False)

        # General words
        self._add_func( 'PRINT', self._print, False)

    def _add_func(self, name, action, immediate):
        self.context[name] = ForthRecord(
            name=name,
            immediate=immediate,
            isNative=True,
            content=action
        )

    def eval(self, iterator):
        self.eval_stack.append(SafeIterator(iterator))
        while len(self.eval_stack) > 0:
            it = self.eval_stack[-1]
            sym = it.next()
            if sym is None:
                self.eval_stack.pop()
                self.mode = "EXECUTE" if len(self.eval_stack)>1 else "INTERPRET"
            else:
                self.eval_symbol(sym)

    def eval_symbol(self, sym: tuple):
        t, v = sym
        if self.mode in ["INTERPRET", "EXECUTE"]:
            if t == 0 and v in self.context:
                self.eval_funct(self.context[v])
            else:
                self.stack.append(sym)
        elif self.mode == "COMPILE":
            if t == 0:
                funct = self.context[v]
                if funct.immediate:
                    self.eval_funct(funct)
                    return
            self._current_word.content.append(sym)

    def eval_funct(self, funct: ForthRecord):
        if funct.isNative:
            funct.content(self)
        elif isinstance(funct.content, list):
            self.eval_stack.append(SafeIterator(funct.content))
        else:
            print(f"Unknown word: {funct}")

    def _push(self):
        # Get from input stream
        it = self.eval_stack[0]
        sym = it.next()
        self.stack.append(sym)

    def _drop(self):
        self.stack.pop()

    def _dup(self):
        self.stack.append(self.stack[-1])

    def _over(self):
        self.stack.append(self.stack[-2])

    def _swap(self):
        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

    def _rot(self):
        self.stack.append(self.stack.pop(-3))

    def _begin_word(self):
        it = self.eval_stack[-1]
        sym = it.next()
        if sym is None:
            raise Exception("Unexpected end of stream!")
        self.mode = "COMPILE"
        self._current_word = ForthRecord(list(), False)
        self.context[sym[1]] = self._current_word

    def _end_word(self):
        self.mode = "EXECUTE"
        self._current_word = None

    def _set_immediate(self):
        if self._current_word.immediate:
            print("Current word is already immediate!")
        self._current_word.immediate = True

    def _math_sum(self):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b + a)

    def _math_sub(self):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b - a)

    def _math_mul(self):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b * a)

    def _math_div(self):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b / a)

    def _math_mod(self):
        a, b = self.stack.pop(), self.stack.pop()
        self.stack.append(b % a)

    def _print(self):
        print(self.stack.pop()[1])

    def _branch(self):
        if self.mode == "INTERPRET":
            raise Exception("Word BRANCH not allowed in interpretation mode")
        elif self.mode == "COMPILE":
            self._current_word.content.append((0, "BRANCH"))
        else:
            # FFFOCK!!!!!
            # This is more complicated then I thought!
            pass



if __name__ == "__main__":
    test()
