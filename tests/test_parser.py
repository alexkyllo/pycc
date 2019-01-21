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
    TokenDouble,
    TokenString,
)

from parser import (
    Constant,
    Variable,
    BinaryOp,
    IfStatement,
    AssignmentStatement,
    ReturnStatement,
    Function,
    Program,
    parse_statement,
    parse,
)

class TestParser(unittest.TestCase):
    def testParseAssignmentStatement(self):
        tokens = [
            TokenIdentifier('a'),
            TokenAssignmentOperator('='),
            TokenInteger('1'),
            TokenSemicolon(';'),
        ]

        stmt = parse_statement(tokens)

        self.assertEqual(str(stmt), "AssignmentStatement a = 1")

if __name__ == '__main__':
    unittest.main()
