import os
import sys
import re

class Token():
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)
        self.value = None

    def lex(self, string):
        matched = self.pattern.match(string)
        if matched:
            self.value = matched.group()
            self.start = matched.start()
            self.end = matched.end()

    def __str__(self):
        return "{0} {1}".format(self.__class__.__name__, self.value)

class TokenKeyword(Token):
    def __init__(self):
        super().__init__((
            "auto|break|case|char|const|continue|default|do|"
            "double|else|enum|extern|float|for|goto|if|int|"
            "long|register|return|short|signed|sizeof|static|"
            "struct|switch|typedef|union|unsigned|void|volatile|while"
        ))

class TokenOpenBrace(Token):
    def __init__(self):
        super().__init__('{')

class TokenCloseBrace(Token):
    def __init__(self):
        super().__init__('}')

class TokenOpenParen(Token):
    def __init__(self):
        super().__init__('\(')

class TokenCloseParen(Token):
    def __init__(self):
        super().__init__('\)')

class TokenSemicolon(Token):
    def __init__(self):
        super().__init__(';')

class TokenAssignmentOperator(Token):
    def __init__(self):
        super().__init__('[<]{2}=|[>]{2}=|[\+\-\*\/%\&\^\!\|]?[=](?!=)')

class TokenArithmeticOperator(Token):
    def __init__(self):
        super().__init__('[+]{2}|[-]{2}|[\+\-\*\/%]')

class TokenRelationalOperator(Token):
    def __init__(self):
        super().__init__('[=\!\>\<][=]|[<>]')

class TokenLogicalOperator(Token):
    def __init__(self):
        super().__init__('&{2}|\|{2}|\!(?!=)')

class TokenIdentifier(Token):
    def __init__(self):
        super().__init__('[a-zA-Z_][a-zA-Z0-9_]*')

class TokenInteger(Token):
    def __init__(self):
        super().__init__('[0-9]+(?!\.)')

    def lex(self, string):
        super().lex(string)
        if self.value:
            self.value = int(self.value)

class TokenDouble(Token):
    def __init__(self):
        super().__init__('[0-9]*\.?[0-9]+')

    def lex(self, string):
        super().lex(string)
        if self.value:
            self.value = float(self.value)

class TokenString(Token):
    def __init__(self):
        super().__init__('"\w+"')

def lex(input_string):
    token_types = (
        TokenKeyword,
        TokenOpenBrace,
        TokenCloseBrace,
        TokenOpenParen,
        TokenCloseParen,
        TokenSemicolon,
        TokenAssignmentOperator,
        TokenArithmeticOperator,
        TokenRelationalOperator,
        TokenLogicalOperator,
        TokenIdentifier,
        TokenInteger,
        TokenDouble,
        TokenString,
    )

    tokens = []
    while len(input_string) > 0:
        for tok_type in token_types:
            token = tok_type()
            token.lex(input_string)
            if token.value:
                tokens.append(token)
                end = token.end
                break
            else:
                end = 1
        input_string = input_string[end:]
    return tokens

# Parser
# AST node classes

class Constant():
    '''A constant value'''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Constant {0}".format(self.value)

class Variable():
    '''A variable'''
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return "Variable {0} = {1}".format(self.name, self.value)

class BinaryOp():
    ''' An infix expression'''
    def __init__(self, operator, lhs, rhs):
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "BinaryOp {0} {1} {2}".format(self.operator, self.lhs, self.rhs)

class IfStatement():
    ''' An if statement'''
    def __init__(self, condition, body, else_body):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __str__(self):
        return "IfStatement {0} {1} {2}".format(self.condition, self.body, self.else_body)

class AssignmentStatement():
    ''' An assignment statement'''
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "AssignmentStatement {0} = {1}".format(self.lhs, self.rhs)

class ReturnStatement():
    ''' A return statement'''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "ReturnStatement {0}".format(self.value)

class Function():
    ''' A function contains a list of statements'''
    def __init__(self, statements):
        self.statements = statements

    def __str__(self):
        return "Function {0}".format(str(self.statements))

class Program():
    ''' A Program contains a list of functions'''
    def __init__(self, functions):
        self.functions = functions

    def __str__(self):
        return "Program {0}".format(str(self.functions))


def parse_statement(tokens):
    is_return = (tokens[0][0] == "keyword_return")
    is_return_value =  (tokens[1][0] in ("identifier", "integer", "double"))

    is_assign = (
        tokens[0][0] == "identifier"
    ) and (
        tokens[1][0] == "assignment"
    ) and (
        tokens[2][0] in ("identifier", "integer", "double")
    )

    if (is_return and is_return_value):
        has_semi = (tokens[2][0] == "semicolon")
        if (not has_semi):
            raise Exception("Token ; expected")
        else:
            return ReturnStatement(value = tokens[1][1])
    elif (is_assign):
        has_semi = (tokens[3][0] == "semicolon")
        if (not has_semi):
            raise Exception("Token ; expected")
        else:
            return AssignmentStatement(lhs = tokens[0][1], rhs = tokens[2][1])

def parse(tokens):
    return tokens

def codegen(ast):
    return ast

# if __name__ == '__main__':
#     source_file = sys.argv[1]
#     assembly_file = os.path.splitext(source_file)[0] + '.s'

#     with open(source_file, 'r') as infile, open(assembly_file, 'w') as outfile:
#         source = infile.read().strip()
#         assembly = codegen(parse(tokenize(source)))
#         outfile.write(str(assembly))
