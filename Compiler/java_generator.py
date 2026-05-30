from type_inference import infer_type, infer_input_type, symbol_table

def generate_java(ast):
    code = [
        "import java.util.Scanner;",
        "",
        "public class Main {",
        "    public static void main(String[] args) {",
        "        Scanner sc = new Scanner(System.in);"
    ]

    indent = 2
    declared = set()

    for node in ast:

        if node[0] == "PRINT":
            code.append("    " * indent + f'System.out.println({node[1]});')

        elif node[0] == "INPUT":
            var = node[1]
            dtype = infer_input_type(var)
            symbol_table[var] = dtype

            if dtype == "int":
                code.append("    " * indent + f'int {var} = sc.nextInt();')
            elif dtype == "float":
                code.append("    " * indent + f'float {var} = sc.nextFloat();')
            else:
                code.append("    " * indent + f'String {var} = sc.next();')

        elif node[0] == "MULTI_INPUT":
            for v in node[1]:
                dtype = infer_input_type(v)
                symbol_table[v] = dtype

                if dtype == "int":
                    code.append("    " * indent + f'int {v} = sc.nextInt();')
                elif dtype == "float":
                    code.append("    " * indent + f'float {v} = sc.nextFloat();')
                else:
                    code.append("    " * indent + f'String {v} = sc.next();')

        elif node[0] == "ASSIGN":
            var, val = node[1], node[2]
            dtype = infer_type(val)
            symbol_table[var] = dtype
            code.append("    " * indent + f'{dtype} {var} = {val};')

        elif node[0] == "IF":
            code.append("    " * indent + f'if ({node[1]})')

        elif node[0] == "ELSE":
            code.append("    " * indent + "else")

        elif node[0] == "WHILE":
            code.append("    " * indent + f'while ({node[1]})')

        elif node[0] == "FOR":
            code.append("    " * indent + f'for (int {node[1]}={node[2]}; {node[1]}<{node[3]}; {node[1]}++)')

        elif node[0] == "BLOCK_START":
            code.append("    " * indent + "{")
            indent += 1

        elif node[0] == "BLOCK_END":
            indent -= 1
            code.append("    " * indent + "}")

    code.append("    }")
    code.append("}")
    return "\n".join(code)