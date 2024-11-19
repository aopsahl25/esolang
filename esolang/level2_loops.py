import lark
import esolang.level1_statements


grammar = esolang.level1_statements.grammar + r"""
    %extend start: forloop | whileloop | ifstmt | continue_stmt | is_prime_call

    forloop: "for" NAME "in" range block
    whileloop: "while" expression block
    ifstmt: "if" expression block ("else" block)?
    continue_stmt: "continue" -> continue_stmt
    is_prime_call: "is_prime" "(" expression ")"

    range: "range" "(" expression ("," expression)? ")"
    expression: NUMBER   -> number
            | NAME     -> var
            | expression "+" expression -> add
            | expression "-" expression -> sub
            | expression "*" expression -> mul
            | expression ">" expression -> gt
            | expression "<" expression -> lt
            | expression "%" expression  -> mod
            | expression "==" expression -> eq
            | expression "and" expression -> and_expr
            | expression "!=" expression -> neq
            | "(" expression ")" -> parens
"""

parser = lark.Lark(grammar)

class ContinueException(Exception):
    pass

class Interpreter(esolang.level1_statements.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("for i in range(10) {i}"))
    9
    >>> interpreter.visit(parser.parse("for i in range(10+5) {i}"))
    14
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}"))
    45
    >>> interpreter.visit(parser.parse("a=0; for i in range(10+5) {a = a + i}"))
    105
    >>> interpreter.visit(parser.parse("a=0; for i in range(5,10) {a = a + i}"))
    35
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}; a"))
    45
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}; i"))
    Traceback (most recent call last):
        ...
    ValueError: Variable i undefined

    >>> interpreter.visit(parser.parse("a=0; while a < 5 {a = a + 1}"))
    5
    >>> interpreter.visit(parser.parse("b=0; while b < 3 {b = b + 1}; b"))
    3
    >>> interpreter.visit(parser.parse("x=10; while x > 0 {x = x - 1}"))
    0

    >>> interpreter.visit(parser.parse("if 2 > 1 {5}"))
    5
    >>> interpreter.visit(parser.parse("if (2-7) > 1 {5} else {10}"))
    10
    >>> interpreter.visit(parser.parse("a = 5; if a > 3 {a = a * 2} else {a = a + 1}; a"))
    10
    >>> interpreter.visit(parser.parse("a = -7; if a > 3 {a = a * 2} else {a = a + 1}; a"))
    -6
    >>> interpreter.visit(parser.parse("a=15; is_prime(a)"))
    False
    >>> interpreter.visit(parser.parse("a=29; is_prime(a)"))
    True
    '''
    
    def range(self, tree):
        if len(tree.children) == 1:
            stop_value = self.visit(tree.children[0])  
            return list(range(stop_value)) 
        elif len(tree.children) == 2:
            start_value = self.visit(tree.children[0])  
            stop_value = self.visit(tree.children[1])  
            return list(range(start_value, stop_value))  
        else:
            raise ValueError("Invalid range expression.")

    def forloop(self, tree):
        varname = tree.children[0].value
        xs = self.visit(tree.children[1])  
        self.stack.append({}) 
        result = None  
        for x in xs:
            self.stack[-1][varname] = x 
            try:
                result = self.visit(tree.children[2])  
            except ContinueException:
                continue  
        self.stack.pop()  
        return result  


    def whileloop(self, tree):
        condition = self.visit(tree.children[0])
        result = None
        while condition:
            try:
                result = self.visit(tree.children[1])  
            except ContinueException:
                continue  
            condition = self.visit(tree.children[0])
        return result

    def ifstmt(self, tree):
        condition = bool(self.visit(tree.children[0]))  
        if condition:
            return self.visit(tree.children[1])  
        elif len(tree.children) > 2:
            return self.visit(tree.children[2])  
        return None


    def _get_from_stack(self, name):
        for d in reversed(self.stack):
            if name in d:
                return d[name]
        raise ValueError(f"Variable {name} undefined")
    
    def var(self, tree):
        varname = tree.children[0].value  
        return self._get_from_stack(varname)
    
    def number(self, tree):
        return int(tree.children[0].value)  

    def add(self, tree):
        left, right = tree.children
        return self.visit(left) + self.visit(right)  
    
    def sub(self, tree):
        left, right = tree.children
        return self.visit(left) - self.visit(right) 
    
    def mul(self, tree):
        left, right = tree.children
        return self.visit(left) * self.visit(right)
    
    def mod(self, tree):
        left, right = tree.children
        right_value = self.visit(right)
        if right_value == 0:
            right_value = 2
        return self.visit(left) % right_value

    def eq(self, tree):
        left, right = tree.children
        return self.visit(left) == self.visit(right)

    def neq(self, tree):
        left, right = tree.children
        return self.visit(left) != self.visit(right)

    def parens(self, tree):
        return self.visit(tree.children[0]) 
    
    def lt(self, tree):
        left, right = tree.children
        return self.visit(left) < self.visit(right)
    
    def gt(self, tree):
        left, right = tree.children
        return self.visit(left) > self.visit(right)
    
    def and_expr(self, tree):
        left, right = tree.children
        left_value = self.visit(left)
        if not left_value:
            return False 
        return self.visit(right) 

    def continue_stmt(self, tree):
        raise ContinueException()  
    
    def is_prime_call(self, tree):
        num = self.visit(tree.children[0])  
        if num <= 1:
            return False
        for i in range(2, num):
            if num % i == 0:
                return False
        return True



interpreter = Interpreter()


