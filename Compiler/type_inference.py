symbol_table = {}

def infer_type(value):
    value = value.strip()

    if value in symbol_table:
        return symbol_table[value]

    if value in ["True", "False"]:
        return "bool"

    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        return "string"

    try:
        if "." not in value:
            int(value)
            return "int"
    except:
        pass

    try:
        float(value)
        return "float"
    except:
        pass

    for op in ["+", "-", "*", "/", "%"]:
        if op in value:
            parts = value.split(op)
            types = [infer_type(p.strip()) for p in parts]
            if "float" in types:
                return "float"
            return "int"

    return "int"


def infer_input_type(var):
    var = var.lower()

    if "name" in var or "str" in var or "text" in var:
        return "string"
    elif "price" in var or "float" in var or "avg" in var:
        return "float"
    else:
        return "int"