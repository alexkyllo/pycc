import sys
import os
import unittest

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
            ('identifier', 'a'),
            ('assignment', '='),
            ('integer', '1'),
            ('semicolon', ';')
        ]

        stmt = parse_statement(tokens)

        self.assertEqual(str(stmt), "AssignmentStatement a = 1")

if __name__ == '__main__':
    unittest.main()
