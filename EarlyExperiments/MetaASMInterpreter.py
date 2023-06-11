from math import ceil
from Tokenizer import Tokenizer


def number_handler(token: Tokenizer.Token):
    compact = token.value.replace('_', '')
    if compact.startswith('0b'):
        token.value = int(ceil((len(compact) - 2) / 8)), int(compact[2:], 2)
    elif compact.startswith('0x'):
        token.value = int(ceil((len(compact) - 2) / 2)), int(compact[2:], 16)
    else:
        try:
            value = int(compact)
            if value < 0x100:
                token.value = 1, value
            elif value < 0x10000:
                token.value = 2, value
            elif value < 0x1000000:
                token.value = 3, value
            elif value < 0x100000000:
                token.value = 4, value
        except:
            pass
    return token

lang_definition = [
    ('OPERATOR', r'(?:\+|\-|\*|\/|\%|\~|\&|\||\^|<<|>>)', False),
    ('STRING', r'\'(?:[^\']|\\\')*\'|"(?:[^"]|\\")*"', False),
    ('SUGAR', r"<\d+|\d+>", False),
    ('NUMBER', r'(?:0x[0-9A-F]+|0b[01]+|[-\+]?\d+)', False),
    ('SYMBOL', r"[a-zA-Z\d\.]+", False),
    ('BRACKET', r'[\[\]\(\)]', False),
    ('NEWLINE', r'[\r\n]+', False),
    ('WHITESPACE', r'[\s,]+', True),
    ('ERROR', r'.', False),
]

lang_tokens_handlers = {
    'NUMBER': number_handler
}

lang_tokenizer = Tokenizer(lang_definition, lang_tokens_handlers)


test = '''
symbol A.B.C.NAME [ <1 0xFF 1> ]
macros NAME.A.B.C [ ... ]

    MOV AX, BC
    ADD AX, (9 + 0x15)
    SET BT, 'my other string 0x15'
'''


class MetaASMInterpreter:
    def __init__(self):
        self.tokens = None
        self._handlers = {
            'SUGAR': self._handle_sugar,
            'SYMBOL': self._handle_symbol,
        }
        self._functions = {
            'LEFT': self._funct_left,
            'RIGHT': self._funct_left,
        }

    def eval(self, text):
        self.tokens = lang_tokenizer.tokenize(text)
        while len(self.tokens) > 0:
            token: Tokenizer.Token = self.tokens.pop(0)
            if token.name in self._handlers:
                self._handlers[token.name](token)

    def _handle_sugar(self, token):
        value: str = token.value
        if value.startswith('<'):
            self.tokens[0:0] = [
                Tokenizer.Token('ATOM', 'LEFT', token.span, True),
                Tokenizer.Token('NUMBER', value[1:], token.span, True)
            ]
        elif value.endswith('>'):
            self.tokens[0:0] = [
                Tokenizer.Token('ATOM', 'RIGHT', token.span, True),
                Tokenizer.Token('NUMBER', value[:-1], token.span, True)
            ]

    def _handle_symbol(self, token: Tokenizer.Token):
        value: str = token.value
        if value in self._functions:
            self._functions[value](token)
        else:
            raise Exception(f'Error at {token.span}: unknown symbol \'{value}\'!')

    def _funct_left(self, token: Tokenizer.Token):
        arg: Tokenizer.Token = self.tokens[0]
        if arg.name != 'NUMBER':
            raise Exception(f'Error at {arg.span}: Expect number! But find {arg.name} instead!')
        self.tokens.pop(0)

    def _funct_right(self, token: Tokenizer.Token):
        arg: Tokenizer.Token = self.tokens[0]
        if arg.name != 'NUMBER':
            raise Exception(f'Error at {arg.span}: Expect number! But find {arg.name} instead!')
        self.tokens.pop(0)


if __name__ == "__main__":
    MetaASMInterpreter()
