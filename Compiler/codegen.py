from type_inference import infer_type, infer_input_type, symbol_table

def generate_cpp(ast):
    code = ["#include <iostream>", "using namespace std;", "", "int main() {"]
    indent = 1
    declared = set()

    for node in ast:

        if node[0] == "PRINT":
            code.append("    " * indent + f'cout << {node[1]} << endl;')

        elif node[0] == "INPUT":
            var = node[1]
            dtype = infer_input_type(var)
            symbol_table[var] = dtype

            if var not in declared:
                code.append("    " * indent + f'{dtype} {var};')
                declared.add(var)

            code.append("    " * indent + f'cin >> {var};')

        elif node[0] == "MULTI_INPUT":
            vars = node[1]
            for v in vars:
                dtype = infer_input_type(v)
                symbol_table[v] = dtype
                if v not in declared:
                    code.append("    " * indent + f'{dtype} {v};')
                    declared.add(v)

            code.append("    " * indent + 'cin >> ' + " >> ".join(vars) + ';')

        elif node[0] == "ASSIGN":
            var, val = node[1], node[2]
            dtype = infer_type(val)
            symbol_table[var] = dtype

            if var not in declared:
                code.append("    " * indent + f'{dtype} {var} = {val};')
                declared.add(var)
            else:
                code.append("    " * indent + f'{var} = {val};')

        elif node[0] == "IF":
            code.append("    " * indent + f'if ({node[1]})')

        elif node[0] == "ELSE":
            code.append("    " * indent + "else")

        elif node[0] == "WHILE":
            code.append("    " * indent + f'while ({node[1]})')

        elif node[0] == "FOR":
            var, start, end = node[1], node[2], node[3]
            code.append("    " * indent + f'for (int {var}={start}; {var}<{end}; {var}++)')

        elif node[0] == "BLOCK_START":
            code.append("    " * indent + "{")
            indent += 1

        elif node[0] == "BLOCK_END":
            indent -= 1
            code.append("    " * indent + "}")

    code.append("    return 0;")
    code.append("}")
    return "\n".join(code)