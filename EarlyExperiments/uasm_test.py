from ByteBuilder import ByteBuilder
from MetaASM import MetaASM


def main():
    buffer = ByteBuilder(10)
    print(buffer.content)
    buffer.append(b'\x01')
    print(buffer.content)
    buffer.append(b'\x0A\x0B\x0C')
    print(buffer.content)
    buffer.seek(-2, 'e')
    buffer.append(b'\x01\x02\x03\x04\x05')
    print(buffer.content)
    buffer.seek(5)
    buffer.append(b'\x01')
    print(buffer.content)


def bytes_test():
    for i in range(0, 512, 1):
        print(f"{i}: {i.to_bytes(4, 'big')}")


if __name__ == "__main__":
    main()
    bytes_test()
