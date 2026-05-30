from lexer import tokenize
from parser import parse
from codegen import generate_cpp

def main():
    with open("input.py", "r") as f:
        lines = f.readlines()

    tokens = tokenize(lines)
    ast = parse(lines)
    cpp_code = generate_cpp(ast)

    with open("output.cpp", "w") as f:
        f.write(cpp_code)

    print("✅ Conversion complete! Check output.cpp")

if __name__ == "__main__":
    main()