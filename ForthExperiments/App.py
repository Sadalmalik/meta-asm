def input_stream():
    active = True
    while active:
        line = input()
        words = line.split()
        for word in words:
            interrupt = yield word
            if interrupt:
                print(f"Interrupted after word: {word}")
                active = False
                break
    yield None


def main():
    print("Test:")
    stream = input_stream()
    w = next(stream)
    print(f"  0: {w}")
    for i in range(1, 10):
        w = stream.send(False)
        print(f"  {i}: {w}")
    w = stream.send(True)
    print(f"  last: {w}")


if __name__ == "__main__":
    main()

