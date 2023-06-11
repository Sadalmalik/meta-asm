

def bf_compile(name, code):
    lines = []
    stack = []
    counter = 0
    lines.append(f"# Program {name}")
    for c in code:
        if c == '+':
            lines.append(f"        INC")
        if c == '-':
            lines.append(f"        DEC")
        if c == '>':
            lines.append(f"        NXT")
        if c == '<':
            lines.append(f"        LST")
        if c == '[':
            counter += 1
            l_name = f"L{counter:0>3}"
            r_name = f"R{counter:0>3}"
            stack.append((l_name, r_name))
            lines.append(f"@ {l_name}")
            lines.append(f"        BGN {r_name}")
        if c == ']':
            l_name, r_name = stack.pop()
            lines.append(f"        END {l_name}")
            lines.append(f"@ {r_name}")
            if 0 == len(stack):
                lines.append("")
        if c == '.':
            lines.append(f"        OUT")
        if c == ',':
            lines.append(f"        INP")
    lines.append(f"        HLT")
    lines.append(f"# End of program {name}")
    print("\n".join(lines))


bf_hello_world = """
>++++++++[<+++++++++>-]<.
>++++[<+++++++>-]<+.
+++++++.
.
+++.
>>++++++[<+++++++>-]<++.
------------.
>++++++[<+++++++++>-]<+.
<.
+++.
------.
--------.
>>>++++[<++++++++>-]<+.
"""

test = """
[]
[[]]
[[][]]
[[[]]]
"""


bf_fibbonachi = """
>+>+<<
++++++++++
[.>

[->>+<<]
>[-<+>>+<]
>[-<+>]
<<.

<-]
"""

if __name__ == "__main__":
    # bf_compile("++[->[-]<]")
    bf_compile("Hello, World!", bf_hello_world)
    # bf_compile("Fibbonachi", bf_fibbonachi)
    # bf_compile(test)
