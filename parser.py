import lexer
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
