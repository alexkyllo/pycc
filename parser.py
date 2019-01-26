from lexer import (
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
        return "(UnaryOp {0} {1})".format(self.operator, self.operand)

class BinaryOperationExpression():
    ''' An infix expression'''
    def __init__(self, operator, lhs, rhs):
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "(BinaryOp {0} {1} {2})".format(self.operator, self.lhs, self.rhs)

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
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "(ReturnStatement {0})".format(self.value)

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

class Program():
    ''' A Program contains a list of functions'''
    def __init__(self, functions):
        self.functions = functions

    def __str__(self):
        return "(Program {0})".format(str(self.functions))

def parse_constant(tokens):
    if any(isinstance(tokens[0], x) for x in (
            TokenIdentifier,
            TokenInteger,
            TokenFloat,
            TokenString,
    )):
        node = Constant(tokens[0].value)
    else:
        node = None

    return node

def parse_identifier_expression(tokens):
    return parse_variable(tokens)

def parse_paren(tokens):
    tokens.pop(0) # swallow (
    expr = parse_expression(tokens)


def parse_binary_operation_rhs(tokens):

    if isinstance(tokens[0], TokenOpenParen):
        exp = parse_binary_operation_expression(tokens[1:])
        if not isinstance(tokens[4], TokenCloseParen):
            raise Exception("Token ) expected")
        return exp
    elif any(isinstance(tokens[1], x) for x in (
            TokenArithmeticOperator,
            TokenRelationalOperator,
            TokenLogicalOperator,
    )):
        return Const(tokens[1].value)
    else:
        raise Exception("Expression must be a constant or a ")

# 1 + 2
# (1 + 1) * 2 -> (* (+ 1 1) 2)
# 1 + (1 * 2)
# 1 + 1 * 2 -> (+ 1 (* 1 2))
# 1 + (1 + (1 * 2))
def parse_binary_operation_expression(tokens):
    if isinstance(tokens[0], TokenIdentifier):
        lhs = parse_identifier_expression(tokens)
    elif any(isinstance(tokens[0], x) for x in (TokenInteger, TokenFloat)):
        lhs = parse_number(tokens)
    elif isinstance(tokens[0], TokenOpenParen):
        lhs = parse_paren(tokens)
    else:
        raise Exception("Unknown token when expecting an expression.")

    while any(isinstance(tokens[1], x) for x in (
            TokenArithmeticOperator,
            TokenRelationalOperator,
            TokenLogicalOperator,
    )):
        rhs = parse_term(tokens[2])
        lhs = BinaryOperationExpression(tokens[1], lhs, rhs)

    return lhs

# def parse_expression(toks):
#     term = parse_term(toks) //pops off some tokens
#     next = toks.peek() //check the next token, but don't pop it off the list yet
#     while next == PLUS or next == MINUS: //there's another term!
#         op = convert_to_op(toks.next())
#         next_term = parse_term(toks) //pops off some more tokens
#         term = BinOp(op, term, next_term)
#         next = toks.peek()
#     return t1

def parse_expression(tokens):
    #To start, just support variables and literals
    token = tokens.pop(0)
    if isinstance(token, TokenIdentifier):
        node = Variable(token.value)
    elif any(isinstance(token, x) for x in (TokenInteger,
                                            TokenFloat,
                                            TokenString,)):
        node = Constant(token.value)
    else:
        raise Exception("Expected Identifier or Constant.")
    return node

def parse_return(tokens):
    keyword_return = tokens.pop(0)
    return_value = parse_expression(tokens)
    semi = tokens.pop(0)
    if not isinstance(semi, TokenSemicolon):
        raise Exception("Token ; expected.")

    return ReturnStatement(return_value)

def parse_assignment(tokens):
    current_token = tokens.pop(0)
    if isinstance(current_token, TokenKeyword):
        lhs = tokens.pop(0)
    elif isinstance(current_token, TokenIdentifier):
        lhs = current_token

    op = tokens.pop(0)
    if not isinstance(op, TokenAssignmentOperator):
        raise Exception("Assignment operator expected.")

    rhs = tokens.pop(0)

    semi = tokens.pop(0)
    if not isinstance(semi, TokenSemicolon):
        raise Exception("Token ; expected.")

    return AssignmentStatement(op = op, lhs = lhs, rhs = rhs)

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
    next_token = tokens[0]
    is_keyword = isinstance(next_token, TokenKeyword)

    if is_keyword:
        if next_token.value == "return":
            node = parse_return(tokens)
        else:
            current_token = tokens.pop(0)

    is_identifier = isinstance(next_token, TokenIdentifier)

    if is_identifier:
        node = parse_assignment(tokens)

    return node

def parse_variable(tokens):
    if not isinstance(tokens[0], TokenIdentifier):
        raise Exception("Expected identifier")
    current_token = tokens.pop(0)
    return Variable(current_token.value)

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

def parse_function(tokens):
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
