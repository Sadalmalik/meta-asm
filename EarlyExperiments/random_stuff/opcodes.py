
numbers = {
    "INC": 0x2b, # +
    "DEC": 0x2d, # -
    "NXT": 0x3e, # >
    "LST": 0x3c, # <
    "BGN": 0x5b, # [
    "END": 0x5d, # ]
    "OUT": 0x2e, # .
    "INP": 0x2c, # ,
}


def show_opcodes():
    for k, v in numbers.items():
        print(f"{k}: {v:0>8b}")


def show_indexes():
    message = "Hello, world!"
    matrix = []
    for c in message:
        matrix.append(list(f"{ord(c):0>8b}"))
    count = len(matrix)
    for i in range(8):
        out = ""
        for n in range(count):
            out += matrix[n][i]
        print(out)

def show_bits():
    b = b'\x0E\x1F\xBA\x0E\x00\xB4\x09\xCD\x21\xB8\x01\x4C\xCD\x21'
    for n in b:
        print(f"{n:0>8b}")


if __name__ == "__main__":
    # show_opcodes()
    # show_indexes()
    # show_bits()
    # test = b'\x00\x80' or b'\x10\x00'
    # print(test)

    for i in range(255):
        print(f"{i:0>2x} 90 90 90 90 90 90 90 90")
