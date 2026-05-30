from type_inference import infer_type, infer_input_type, symbol_table

def generate_js(ast):
    code = []
    indent = 0
    declared = set()

    for node in ast:

        if node[0] == "PRINT":
            code.append("    " * indent + f'console.log({node[1]});')

        elif node[0] == "INPUT":
            var = node[1]
            dtype = infer_input_type(var)
            symbol_table[var] = dtype

            if dtype == "int":
                code.append("    " * indent + f'let {var} = parseInt(input());')
            elif dtype == "float":
                code.append("    " * indent + f'let {var} = parseFloat(input());')
            else:
                code.append("    " * indent + f'let {var} = input();')

        elif node[0] == "MULTI_INPUT":
            vars = node[1]
            code.append("    " * indent + f'let [{", ".join(vars)}] = input().split(" ");')

        elif node[0] == "ASSIGN":
            code.append("    " * indent + f'let {node[1]} = {node[2]};')

        elif node[0] == "IF":
            code.append("    " * indent + f'if ({node[1]})')

        elif node[0] == "ELSE":
            code.append("    " * indent + "else")

        elif node[0] == "WHILE":
            code.append("    " * indent + f'while ({node[1]})')

        elif node[0] == "FOR":
            code.append("    " * indent + f'for (let {node[1]}={node[2]}; {node[1]}<{node[3]}; {node[1]}++)')

        elif node[0] == "BLOCK_START":
            code.append("    " * indent + "{")
            indent += 1

        elif node[0] == "BLOCK_END":
            indent -= 1
            code.append("    " * indent + "}")

    return "\n".join(code)