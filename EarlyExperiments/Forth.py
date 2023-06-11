

class MetaForth:
    def __init__(self):
        self.stack = []

    def eval(self, text):
        words = text.split()

        while len(words) > 0:
            word = words.pop(0)



def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    return 0


def applyOp(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a // b


def evaluate(tokens):
    val_stack = []
    ops_stack = []
    i = 0

    while i < len(tokens):
        if tokens[i] == ' ':
            i += 1
            continue
        elif tokens[i] == '(':
            ops_stack.append(tokens[i])
        elif tokens[i].isdigit():
            val = 0
            while (i < len(tokens) and
                   tokens[i].isdigit()):
                val = (val * 10) + int(tokens[i])
                i += 1
            val_stack.append(val)
            i -= 1

        elif tokens[i] == ')':
            while len(ops_stack) != 0 and ops_stack[-1] != '(':
                val2 = val_stack.pop()
                val1 = val_stack.pop()
                op = ops_stack.pop()
                val_stack.append(applyOp(val1, val2, op))
            ops_stack.pop()

        else:
            while (len(ops_stack) != 0 and
                   precedence(ops_stack[-1]) >=
                   precedence(tokens[i])):
                val2 = val_stack.pop()
                val1 = val_stack.pop()
                op = ops_stack.pop()
                val_stack.append(applyOp(val1, val2, op))
            ops_stack.append(tokens[i])
        i += 1

    while len(ops_stack) != 0:
        val2 = val_stack.pop()
        val1 = val_stack.pop()
        op = ops_stack.pop()
        val_stack.append(applyOp(val1, val2, op))
    return val_stack[-1]


if __name__ == "__main__":
    print(evaluate("10 + 2 * 6"))
    print(evaluate("100 * 2 + 12"))
    print(evaluate("100 * ( 2 + 12 )"))
    print(evaluate("100 * ( 2 + 12 ) / 14"))
