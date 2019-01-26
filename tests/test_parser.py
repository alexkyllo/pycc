import sys
import os
import unittest

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

from parser import (
    Constant,
    Variable,
    BinaryOperationExpression,
    IfStatement,
    AssignmentStatement,
    ReturnStatement,
    Argument,
    Function,
    Program,
    parse_assignment,
    parse_binary_operation_expression,
    parse_constant,
    parse_function,
    parse_function_argument,
    parse_statement,
    parse_variable,
    parse,
)

class TestParser(unittest.TestCase):
    def test_parse_assignment_statement(self):
        tokens = [
            TokenIdentifier('a'),
            TokenAssignmentOperator('='),
            TokenInteger('1'),
            TokenSemicolon(';'),
        ]

        stmt = parse_assignment(tokens)

        self.assertEqual(str(stmt), "(AssignmentStatement TokenAssignmentOperator = TokenIdentifier a TokenInteger 1)")

    def test_parse_constant(self):
        tokens = [
            TokenInteger('1')
        ]

        stmt = parse_constant(tokens)

        self.assertEqual(str(stmt), "(Constant 1)")

    def test_parse_variable(self):
        tokens = [
            TokenIdentifier('a'),
            TokenAssignmentOperator('='),
            TokenInteger('2'),
        ]

        var = parse_variable(tokens)

        self.assertEqual(str(var), "(Variable a)")

    def test_parse_function_argument(self):
        tokens = [
            TokenKeyword('int'),
            TokenIdentifier('a'),
            TokenKeyword('int'),
            TokenIdentifier('b')
        ]

        args = parse_function_argument(tokens)

        self.assertEqual(
            str(args),
            "(Argument TokenKeyword int (Variable a))"
        )

    def test_parse_binary_operation_1(self):
        tokens = [
            TokenIdentifier('a'),
            TokenRelationalOperator('>'),
            TokenInteger('2'),
        ]

        expr = parse_binary_operation_expression(tokens)

        self.assertEqual(str(expr), "(BinaryOp > (Identifier a) (Constant 2))")

    def test_parse_binary_operation_2(self):
        tokens = [
            TokenIdentifier('a'),
            TokenArithmeticOperator('+'),
            TokenInteger('1'),
            TokenArithmeticOperator('*'),
            TokenInteger('2'),
            # a + 1 * 2 => (+ a (* 1 2))
        ]

        expr = parse_binary_operation_expression(tokens)

        self.assertEqual(
            str(expr),
            "(BinaryOperationExpression + a (BinaryOperationExpression * 1 2))"
        )

    def test_parse_binary_operation_2(self):
        tokens = [
            TokenIdentifier('a'),
            TokenArithmeticOperator('+'),
            TokenInteger('1'),
            TokenArithmeticOperator('+'),
            TokenInteger('2'),
            # a + 1 + 2 => (+ (+ a 1) 2)
        ]

        expr = parse_binary_operation_expression(tokens)

        self.assertEqual(
            str(expr),
            "(BinaryOperationExpression + (BinaryOperationExpression + a 1) 2))"
        )

if __name__ == '__main__':
    unittest.main()
