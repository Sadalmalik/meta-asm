from math import ceil
from ByteBuilder import ByteBuilder


class MetaASM:
    def __init__(self):
        self._buffer = ByteBuilder()
        self._items = None
        self._symbols = {}
        self._pointers = {}
        self._index = 0

    def assemble_file(self, path):
        with open(path, "r", encoding="utf8") as file:
            text = file.read()
        self.assemble(text)

    def assemble(self, text):
        self._items = self.parse(text)
        while len(self._items) > 0:
            item = self._items.pop(0)
            directive = item[0]
            if directive == 'include':
                # include assemble file
                with open(item[1], "r", encoding="utf8") as file:
                    text = file.read()
                self._items = self.parse(text) + self._items
            elif directive == 'offset':
                # set bytes offset for assemble
                if not isinstance(item[1], tuple):
                    raise Exception("offset must be number!")
                self._buffer.seek(item[1][1])
            elif directive == 'symbol':
                # define symbol
                name = item[1]
                if name in self._symbols:
                    raise Exception(f"Symbol {name} already defined! You must un-define it before redefinition!")
                self._symbols[name] = (item[2], item[3])
            elif directive == 'forget':
                # forget symbol
                name = item[1]
                if name not in self._symbols:
                    raise Exception(f"Symbol {name} not defined! You must define it before un-define!")
                del self._symbols[name]
            elif directive.startswith(':'):
                # define pointer
                name = '.'+directive[1:]
                if name in self._pointers:
                    raise Exception(f"Pointer {name} already defined!")
                self._pointers[name] = {'index': self._index, 'refers': []}
            else:
                # interpret symbols and pointers
                for word in item:
                    if isinstance(word, tuple):
                        word[1].to_bytes(word[0], 'big')
                    elif word in self._pointers:
                        pass
                    elif word in self._symbols:
                        mode, value = self._symbols[word]
                        if mode == 'OR'
                    else:
                        raise Exception(f"Unknown symbol '{name}'!")
        # Complete

    def parse(self, text):
        items = []
        lines = text.splitlines()
        for line in lines:
            line = line.strip()
            if line == '':
                continue
            if '#' in line:
                if line.startswith('#'):
                    continue
                idx = line.index('#')
                if idx > -1:
                    line = line[0:idx]
            if ';' in line:
                sub_lines = line.split(';')
                for sub_line in sub_lines:
                    parts = [self._parse_number(p.strip()) for p in sub_line.split()]
                    items.append(parts)
            else:
                parts = [self._parse_number(p.strip()) for p in line.split()]
                items.append(parts)
        return items

    def parse_primitive(self, raw: str):
        number = self.parse_number(raw)
        if isinstance(number, tuple):
            return number

        string = self.parse_number(raw)
        if isinstance(string, tuple):
            return string

        return 'symbol', raw

    def parse_string(self, raw: str):
        pass

    def parse_number(self, raw: str):
        compact = raw.replace('_', '')
        if compact.startswith('0b'):
            return 'number', int(ceil((len(compact)-2)/8)), int(compact[2:], 2)
        elif compact.startswith('0x'):
            return 'number', int(ceil((len(compact)-2)/2)), int(compact[2:], 16)
        else:
            try:
                value = int(compact)
                if value < 0x100:
                    return 'number', 1, value
                elif value < 0x10000:
                    return 'number', 2, value
                elif value < 0x1000000:
                    return 'number', 3, value
                elif value < 0x100000000:
                    return 'number', 4, value
            except:
                pass
        return False

