class PrintNode:
    def __init__(self, value):
        self.value = value


class AssignNode:
    def __init__(self, var, value):
        self.var = var
        self.value = value