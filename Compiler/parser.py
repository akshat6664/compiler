def get_indent(line):
    return len(line) - len(line.lstrip())


def parse(lines):
    ast = []
    stack = [0]

    for line in lines:
        if not line.strip():
            continue

        indent = get_indent(line)
        line = line.strip()

        while indent < stack[-1]:
            ast.append(("BLOCK_END", "}"))
            stack.pop()

        if line.startswith("if"):
            ast.append(("IF", line[line.find("(")+1 : line.rfind(")")]))
            ast.append(("BLOCK_START", "{"))
            stack.append(indent + 4)

        elif line.startswith("else"):
            ast.append(("ELSE", None))
            ast.append(("BLOCK_START", "{"))
            stack.append(indent + 4)

        elif line.startswith("while"):
            ast.append(("WHILE", line[6:-1]))
            ast.append(("BLOCK_START", "{"))
            stack.append(indent + 4)

        elif line.startswith("for"):
            parts = line.split()
            var = parts[1]
            r = line[line.find("range(")+6 : line.find(")")]
            vals = r.split(",")
            start = vals[0].strip() if len(vals) > 1 else "0"
            end = vals[-1].strip()
            ast.append(("FOR", var, start, end))
            ast.append(("BLOCK_START", "{"))
            stack.append(indent + 4)

        elif "input()" in line and "=" in line and "," in line:
            vars = [v.strip() for v in line.split("=")[0].split(",")]
            ast.append(("MULTI_INPUT", vars))

        elif "input()" in line and "=" in line:
            ast.append(("INPUT", line.split("=")[0].strip()))

        elif line.startswith("print"):
            ast.append(("PRINT", line[6:-1]))

        elif "=" in line:
            var, val = line.split("=", 1)
            ast.append(("ASSIGN", var.strip(), val.strip()))

    while len(stack) > 1:
        ast.append(("BLOCK_END", "}"))
        stack.pop()

    return ast