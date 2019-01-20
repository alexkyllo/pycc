import os
import sys
import re

# Tokenizer
def tokenize(input):
    token_definitions = (
        ('keyword_int', 'int'),
        ('keyword_return','return'),
        ('open_brace', '{'),
        ('close_brace', '}'),
        ('open_paren', '\('),
        ('close_paren', '\)'),
        ('semicolon', ';'),
        ('identifier', '[a-zA-Z_][a-zA-Z0-9_]*'),
        ('integer', '[0-9]+(?!\.)'),
        ('double', '[0-9]*\.?[0-9]+')
    )

    tokens = []

    input_string = input

    while len(input_string) > 0:
        for tokdef in token_definitions:
            regex_string = tokdef[1]
            regex = re.compile(regex_string)
            match_result = regex.match(input_string)
            if match_result:
                tokens.append((tokdef[0], match_result.group()))
                end = match_result.end()
                break
            else:
                end = 1
        input_string = input_string[end:]

    return tokens

# Parser
# AST component classes

class Constant():
    '''A constant value'''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str("Constant {0}".format(self.value))

class Variable():
    '''A variable'''
    def __init__(self, name, value):
        self.name = name
        self.value = value

class BinaryOp():
    ''' An infix expression'''
    def __init__(self, operator, lhs, rhs):
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str("BinaryOp {0} {1} {2}".format(self.operator, self.lhs, self.rhs))

class IfStatement():
    ''' An if statement'''
    def __init__(self, condition, body, else_body):
        self.condition = condition
        self.body = body
        self.else_body = else_body

class AssignmentStatement():
    ''' An assignment statement'''
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class ReturnStatement():
    ''' A return statement'''
    def __init__(self, value):
        self.value = value

class Function():
    ''' A function contains a list of statements'''
    def __init__(self, statements):
        self.statements = statements

class Program():
    ''' A Program contains a list of functions'''
    def __init__(self, functions):
        self.functions = functions

def parse(tokens):
    return tokens

def codegen(ast):
    return ast

if __name__ == '__main__':
    source_file = sys.argv[1]
    assembly_file = os.path.splitext(source_file)[0] + '.s'

    with open(source_file, 'r') as infile, open(assembly_file, 'w') as outfile:
        source = infile.read().strip()
        assembly = codegen(parse(tokenize(source)))
        outfile.write(str(assembly))
