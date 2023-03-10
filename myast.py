class AST:
    pass

class Node:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class FuncCall(Node):
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg
    
    def __repr__(self):
        return f"{self.func}({self.arg})"

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class Var(AST):
    def __init__(self, name, value):
        self.name = name
        self.value = value