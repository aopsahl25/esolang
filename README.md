# esolang ![](https://github.com/mikeizbicki/esolang/workflows/tests/badge.svg)

A simple esolang for experimenting with different syntax and semantics of programming languages.

Examples demonstrating functionality:

For Loops

```
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
```

While Loops

```
    >>> interpreter.visit(parser.parse("a=0; while a < 5 {a = a + 1}"))
    5
    >>> interpreter.visit(parser.parse("b=0; while b < 3 {b = b + 1}; b"))
    3
    >>> interpreter.visit(parser.parse("x=10; while x > 0 {x = x - 1}"))
    0
```

If Statements

```
    >>> interpreter.visit(parser.parse("if 2 > 1 {5}"))
    5
    >>> interpreter.visit(parser.parse("if (2-7) > 1 {5} else {10}"))
    10
    >>> interpreter.visit(parser.parse("a = 5; if a > 3 {a = a * 2} else {a = a + 1}; a"))
    10
    >>> interpreter.visit(parser.parse("a = -7; if a > 3 {a = a * 2} else {a = a + 1}; a"))
    -6
```
Computing Prime Numbers

Grammar for identifying prime numbers: 

```
    %extend start: forloop | whileloop | ifstmt | continue_stmt | is_prime_call

    is_prime_call: "is_prime" "(" expression ")"
```

Function for identifying prime numbers (housed in interpreter class): 

```
    def is_prime_call(self, tree):
        num = self.visit(tree.children[0])  
        if num <= 1:
            return False
        for i in range(2, num):
            if num % i == 0:
                return False
        return True
```

Test cases identifying if a number is prime:

```
>>> interpreter.visit(parser.parse("a=15; is_prime(a)"))
False
>>> interpreter.visit(parser.parse("a=29; is_prime(a)"))
True
```

