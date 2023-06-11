
def main():
    print("a = int(input('Enter number 1: '))")
    print("b = int(input('Enter number 2: '))")
    print("op = int(input('Choose operation (+, -, * or /): '))")
    for i in range(10):
        for j in range(10):
            for k in ['+', '-', '*', '/']:
                print(f"if a == {i} and if b == {j} and op == {k}:")
                res = i+j
                if k == '-':
                    res = i-j
                elif k == '*':
                    res = i*j
                elif k == '/':
                    if j == 0:
                        print(f"    print(\"{i} {k} {j} = Error! Division by zero!\")")
                        continue
                    res = i / j
                print(f"    print(\"{i} {k} {j} = {res}\")")


if __name__ == "__main__":
    main()
