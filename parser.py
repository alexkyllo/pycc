from lexer import (
    TokenKeyword,
    TokenOpenBrace,
    TokenCloseBrace,
    TokenOpenParen,
    TokenCloseParen,
    TokenSemicolon,
    TokenAssignmentOperator,
    TokenAdditionOperator,
    TokenMultiplicationOperator,
    TokenIncrementOperator,
    TokenEqualityOperator,
    TokenInequalityOperator,
    TokenLogicalOperator,
    TokenIdentifier,
    TokenInteger,
    TokenFloat,
    TokenString,
)

class Constant():
    '''A constant value'''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "(Constant {0})".format(self.value)

class Variable():
    '''A variable'''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "(Variable {0})".format(self.value)

class UnaryOperationExpression():
    '''A prefix expression'''
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return "(UnaryOp {0} {1})".format(self.operator.value, self.operand)

class BinaryOperationExpression():
    ''' An infix expression'''
    def __init__(self, operator, lhs, rhs):
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "(BinaryOp {0} {1} {2})".format(self.operator.value, self.lhs, self.rhs)

class IfStatement():
    ''' An if statement'''
    def __init__(self, condition, body, else_body):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __str__(self):
        return "(IfStatement {0} {1} {2})".format(self.condition, self.body, self.else_body)

class AssignmentStatement():
    ''' An assignment statement'''
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "(AssignmentStatement {0} {1} {2})".format(self.op, self.lhs, self.rhs)
    def __repr__(self):
        return str(self)

class ReturnStatement():
    ''' A return statement'''
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return "(ReturnStatement {0})".format(self.expression)

    def __repr__(self):
        return str(self)

class Argument():
    ''' A function argument'''
    def __init__(self, type_name, name):
        self.type_name = type_name
        self.name = name

    def __str__(self):
        return "(Argument {0} {1})".format(self.type_name, self.name)

class Function():
    ''' A function contains a list of statements'''
    def __init__(self, return_type, name, arguments=[], statements=[]):
        self.return_type = return_type
        self.name = name
        self.arguments = arguments
        self.statements = statements

    def __str__(self):
        return "(Function {0} {1} ({2}) {3})".format(
            self.return_type,
            self.name,
            self.arguments,
            str(self.statements))

class Call():
    ''' A function call contains a function name and a list of arguments'''
    def __init__(self, name, arguments = []):
        self.name = name
        self.arguments = arguments

    def __str__(self):
        return "(Call {0} ({1}))".format(self.name, self.arguments)

class Program():
    ''' A Program contains a list of functions'''
    def __init__(self, functions):
        self.functions = functions

    def __str__(self):
        return "(Program {0})".format(str(self.functions))

def parse_constant(tokens):
    if any(isinstance(tokens[0], x) for x in (
            TokenInteger,
            TokenFloat,
            TokenString,
    )):
        current_token = tokens.pop(0)
        node = Constant(current_token.value)
    else:
        node = None
    return node

def parse_variable(tokens):
    if isinstance(tokens[0], TokenIdentifier):
        current_token = tokens.pop(0)
        node = Variable(current_token.value)
    else:
        node = None
    return node

def parse_primary(tokens):
    expr = parse_constant(tokens) or parse_variable(tokens)
    if expr:
        return expr
    open_paren = accept(TokenOpenParen, tokens)
    if open_paren:
        expr = parse_expression(tokens)
        expect(TokenCloseParen, tokens)
        return expr

def parse_unary(tokens):
    next_token = tokens[0]
    if any(isinstance(tokens[0], x) for x in (
            TokenLogicalOperator,
            TokenAdditionOperator,
    )):
        operator = (accept(TokenLogicalOperator, tokens)
                    or accept(TokenAdditionOperator, tokens))
        rhs = parse_unary(tokens)
        return UnaryOperationExpression(operator, rhs)
    else:
        return parse_primary(tokens)

def parse_multiplication(tokens):
    expr = parse_unary(tokens)
    next_token = tokens[0]
    while isinstance(next_token, TokenMultiplicationOperator):
        operator = accept(TokenAdditionOperator, tokens)
        rhs = parse_multiplication(tokens)
        expr = BinaryOperationExpression(operator, expr, rhs)
    return expr

def parse_addition(tokens):
    expr = parse_multiplication(tokens)
    next_token = tokens[0]
    while isinstance(next_token, TokenAdditionOperator):
        operator = accept(TokenAdditionOperator, tokens)
        rhs = parse_addition(tokens)
        expr = BinaryOperationExpression(operator, expr, rhs)
    return expr

def parse_comparison(tokens):
    expr = parse_addition(tokens)
    next_token = tokens[0]
    while isinstance(next_token, TokenInequalityOperator):
        operator = accept(TokenInequalityOperator, tokens)
        rhs = parse_comparison(tokens)
        expr = BinaryOperationExpression(operator, expr, rhs)
    return expr

def parse_equality(tokens):
    expr = parse_comparison(tokens)
    next_token = tokens[0]
    while isinstance(next_token, TokenEqualityOperator):
        operator = accept(TokenEqualityOperator, tokens)
        rhs = parse_equality(tokens)
        expr = BinaryOperationExpression(operator, expr, rhs)
    return expr

def parse_expression(tokens):
    expr = parse_equality(tokens)
    return expr

def parse_return(tokens):
    if accept_value(TokenKeyword, 'return', tokens):
        expr = parse_expression(tokens)
        expect(TokenSemicolon, tokens)
        return ReturnStatement(expr)

def accept(tok_type, tokens):
    if isinstance(tokens[0], tok_type):
        return tokens.pop(0)
    else:
        return None

def accept_value(tok_type, tok_value, tokens):
    if isinstance(tokens[0], tok_type) and tokens[0].value == tok_value:
        return tokens.pop(0)
    else:
        return None

def expect(tok, tokens):
    match = accept(tok, tokens)
    if not match:
        raise Exception("Expected token {0}".format(tok.__name__))
    return match

def parse_assignment(tokens):
    lhs = accept(TokenIdentifier, tokens)
    if lhs:
        if accept(TokenAssignmentOperator, tokens):
            rhs = parse_expression(tokens)
            expect(TokenSemicolon, tokens)
            return AssignmentStatement(lhs, rhs)
    return None

def parse_initializing_assignment(tokens):
    # handle initializing assignment statement
    if accept(TokenKeyword, tokens):
        if accept(TokenIdentifier, tokens):
            if accept(TokenAssignmentOperator, tokens):
                expr = parse_expression(tokens)
                expect(TokenSemicolon, tokens)
                return AssignmentStatement(expr)

def parse_function_call(tokens):
    if accept(TokenOpenParen, tokens):
        # handle function call
        args = []
        while not accept(TokenCloseParen, tokens):
            args.append(parse_function_argument(tokens))
            expect(TokenSemicolon, tokens)
        return Call()

def parse_statement(tokens):
    # Declarations
    # int a;
    # Assignment statements:
    # a = 1;
    # int a = 1;
    # Return statements:
    # return a;
    # return a + 1;
    # Other keyword statements:
    # break;
    # continue;
    # check if first token is keyword or identifier name
    stmt = (parse_return(tokens)
            or parse_assignment(tokens)
            or parse_init(tokens)
            or parse_call(tokens))

    return stmt

def parse_function_argument(tokens):
    # does not handle * pointer yet
    current_token = tokens.pop(0)
    if not isinstance(current_token, TokenKeyword):
        raise Exception("Expected argument type declaration")

    type_name = current_token

    if not(isinstance(tokens[0], TokenIdentifier)):
        raise Exception("Expected identifier for argument name")

    name = parse_variable(tokens)

    return Argument(type_name, name)

def parse_function_declaration(tokens):
    current_token = tokens.pop(0)

    if isinstance(current_token, TokenKeyword):
        return_type = current_token
    else:
        raise Exception("Expected return type declaration")

    current_token = tokens.pop(0)
    if isinstance(current_token, TokenIdentifier):
        name = current_token
    else:
        raise Exception("Expected identifier for function name")

    current_token = tokens.pop(0)
    args = []
    if isinstance(current_token, TokenOpenParen):
        while not isinstance(tokens[0], TokenCloseParen):
            args.append(parse_function_argument(tokens))
    else:
        raise Exception("Expected token (")

    tokens.pop(0) # swallow )
    statements = []
    current_token = tokens.pop(0) # should be {
    if isinstance(current_token, TokenOpenBrace):
        while not isinstance(tokens[0], TokenCloseBrace):
            statements.append(parse_statement(tokens))
    else:
        raise Exception("Expected token {")

    return Function(return_type, name, args, statements)


def parse(tokens):
    functions = []
    while len(tokens) > 0:
        functions.append(parse_function(tokens))

    return Program(functions)
