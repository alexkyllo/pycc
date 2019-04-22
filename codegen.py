def generate_return_statement(stmt):
    stmt.expression
    return "movl    ${0}, %eax\nret".format()

def codegen(ast):
    return ast
