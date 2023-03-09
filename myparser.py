from token import Token, INTEGER, FLOAT, FUNCTION, ID, DECIMAL_POINT, PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EXPONENTIATION, FLOOR_DIVIDE, LPAREN, RPAREN, EOF, FACTORIAL
from ast import Num, BinOp, FuncCall, AST, Node, UnaryOp

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type, token_value=None):
        if self.current_token.type == token_type:
            if token_value is None or self.current_token.value == token_value:
                self.current_token = self.lexer.get_next_token()
            else:
                self.error()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            if self.current_token.type == FACTORIAL:
                op = self.current_token
                self.eat(FACTORIAL)
                return UnaryOp(op, Num(token))
            return Num(token)
        elif token.type == FLOAT:
            self.eat(FLOAT)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == EXPONENTIATION:
            self.eat(EXPONENTIATION)
            node = self.factor()
            return BinOp(left=Num(Token(INTEGER, '2')), op=EXPONENTIATION, right=node)
        elif token.type == MODULO:
            self.eat(MODULO)
            node = BinOp(left=node, op=token, right=self.factor())
            return node
            
        elif token.type == ID:
            func_name = self.current_token.value
            self.eat(ID)
            self.eat(LPAREN)
            arg = self.expr()
            self.eat(RPAREN)
            return FuncCall(func_name, arg)
        else:
            self.error()

    def term(self):
        node = self.factor()
        while self.current_token.type in (MULTIPLY, DIVIDE, FLOOR_DIVIDE, EXPONENTIATION, MODULO):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == FLOOR_DIVIDE:
                self.eat(FLOOR_DIVIDE)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == EXPONENTIATION:
                self.eat(EXPONENTIATION)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == MODULO:
                self.eat(MODULO)
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == FACTORIAL:
                self.eat(FACTORIAL)
                print("HI")
                node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node
