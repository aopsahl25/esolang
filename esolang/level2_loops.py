import lark
import esolang.level1_statements


grammar = esolang.level1_statements.grammar + r"""
    %extend start: forloop | whileloop | ifstmt

    forloop: "for" NAME "in" range block
    whileloop: "while" expression block
    ifstmt: "if" expression block ("else" block)?

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
            | "(" expression ")" -> parens
"""

parser = lark.Lark(grammar)

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
    #while statements 
    >>> interpreter.visit(parser.parse("a=0; while a < 5 {a = a + 1}"))
    5
    >>> interpreter.visit(parser.parse("b=0; while b < 3 {b = b + 1}; b"))
    3
    >>> interpreter.visit(parser.parse("x=10; while x > 0 {x = x - 1}"))
    0
    #if statements
    >>> interpreter.visit(parser.parse("if 2 > 1 {5}"))
    5
    >>> interpreter.visit(parser.parse("if (2-7) > 1 {5} else {10}"))
    10
    >>> interpreter.visit(parser.parse("a = 5; if a > 3 {a = a * 2} else {a = a + 1}; a"))
    10
    >>> interpreter.visit(parser.parse("a = -7; if a > 3 {a = a * 2} else {a = a + 1}; a"))
    -6
    '''

    def range(self, tree):
        # Handle range with one argument, e.g., range(10)
        if len(tree.children) == 1:
            stop_value = self.visit(tree.children[0])  # Evaluate the single argument
            return list(range(stop_value))  # From 0 to stop_value-1
        # Handle range with two arguments, e.g., range(5, 10)
        elif len(tree.children) == 2:
            start_value = self.visit(tree.children[0])  # Start of the range
            stop_value = self.visit(tree.children[1])  # End of the range
            return list(range(start_value, stop_value))  # From start to stop_value-1
        else:
            raise ValueError("Invalid range expression.")

    def forloop(self, tree):
        varname = tree.children[0].value  # Get the variable name
        xs = self.visit(tree.children[1])  # Evaluate the range expression
        self.stack.append({})  # Push a new stack frame to track variables
        
        result = None  # Default result to None
        for x in xs:
            self.stack[-1][varname] = x  # Assign the current value to the variable in the loop
            result = self.visit(tree.children[2])  # Evaluate the block
        self.stack.pop()  # Pop the stack frame after loop execution
        return result  # Return the last evaluated result in the block

    def whileloop(self, tree):
    # Get the condition expression (should return a boolean)
        condition = self.visit(tree.children[0])  # Condition expression
        result = None  # Default result to None
    
    # Continue looping while the condition is true
        while condition:
            result = self.visit(tree.children[1])  # Evaluate the block inside the while loop
        # Re-evaluate the condition after the block has executed
            condition = self.visit(tree.children[0])  # Recheck the condition
    
        return result


    def ifstmt(self, tree):
        condition = bool(self.visit(tree.children[0]))  # Ensure condition is a boolean
        print(f"Condition evaluated to: {condition}")
        if condition:
            return self.visit(tree.children[1])  # Evaluate the if block
        elif len(tree.children) > 2:
            return self.visit(tree.children[2])  # Evaluate the else block
        return None


    def var(self, tree):
        varname = tree.children[0].value  # Get the variable name
        if varname not in self.stack[-1]:
            raise ValueError(f"Variable '{varname}' is not defined.")  # This will raise an error if undefined
    
        return self.stack[-1][varname]  # Return the variable value

    def number(self, tree):
        return int(tree.children[0].value)  # Return the integer value

    def add(self, tree):
        left, right = tree.children
        return self.visit(left) + self.visit(right)  # Add the left and right values
    
    def sub(self, tree):
        left, right = tree.children
        return self.visit(left) - self.visit(right)  # Subtract the right from the left
    
    def mul(self, tree):
        left, right = tree.children
        return self.visit(left) * self.visit(right)
    
    def mod(self, tree):
        left, right = tree.children
        return self.visit(left) % self.visit(right)
    
    def eq(self, tree):
        left, right = tree.children
        return self.visit(left) == self.visit(right)

    def parens(self, tree):
        return self.visit(tree.children[0]) 
    
    def lt(self, tree):
        left, right = tree.children
        return self.visit(left) < self.visit(right)
    
    def gt(self, tree):
        left, right = tree.children
        return self.visit(left) > self.visit(right)

#interpreter.visit(parser.parse("for i in range(2,31) {if (i > 1) {for j in range(, i) {if (i % j == 0) {continue}}; i}}"))
# have verified through interpreter.visit(parser.parse("for i in range(2,31) {if (i > 1)...