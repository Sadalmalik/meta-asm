# Original tokenizer is here: https://gist.github.com/codebrainz/ffbd2fde8d44b93c22f0

import re
from collections import namedtuple


class Tokenizer:
    Token = namedtuple('Token', ['name', 'value', 'span', 'internal'])

    def __init__(self, tokens, handlers: dict):
        self.tokens = tokens
        self.handlers = handlers
        self.ignore = set()
        pat_list = []
        for name, pattern, ignore in self.tokens:
            pat_list.append(f'(?P<{name}>{pattern})')
            if ignore:
                self.ignore.add(name)
        final_re = '|'.join(pat_list)
        self.re = re.compile(final_re)
        print(final_re)

    def iter_tokens(self, input, ignore=True):
        for match in self.re.finditer(input):
            if ignore and match.lastgroup in self.ignore:
                continue
            token = Tokenizer.Token(match.lastgroup, match.group(0), match.span(0), False)
            if token.name in self.handlers:
                token = self.handlers[token.name](token)
            yield token

    def tokenize(self, input, ignore_ws=True):
        return list(self.iter_tokens(input, ignore_ws))


# test program
if __name__ == "__main__":
    EXAMPLE_LISP_TOKENS = [
        ('NIL', r"nil|\'()", False),
        ('TRUE', r'true|#t', False),
        ('FALSE', r'false|#f', False),
        ('NUMBER', r'\d+', False),
        ('STRING', r'"(\\.|[^"])*"', False),
        ('SYMBOL', r'[\x21-\x26\x2a-\x7e]+', False),
        ('QUOTE', r"'", False),
        ('LPAREN', r'\(', False),
        ('RPAREN', r'\)', False),
        ('DOT', r'\.', False),
        ('WHITESPACE', r'\s+', True),
        ('ERROR', r'.', False),
    ]
    for t in Tokenizer(EXAMPLE_LISP_TOKENS).iter_tokens('(+ nil 1 2)'):
        print(t)
