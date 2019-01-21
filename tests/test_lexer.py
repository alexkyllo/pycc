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
    lex,
)

class TestLexer(unittest.TestCase):

    def testLexKeyword(self):
        t = lex('int')[0]
        self.assertIsInstance(t, TokenKeyword)
        self.assertEqual(t.value, 'int')

    def testLexDouble(self):
        t = lex('return 1.234;')[1]
        self.assertIsInstance(t, TokenDouble)
        self.assertEqual(t.value, 1.234)

    def testLexInteger(self):
        t = lex('return 2;')[1]
        self.assertIsInstance(t, TokenInteger)
        self.assertEqual(t.value, 2)

    def testLexOpenBrace(self):
        t = lex('{return 1;}')[0]
        self.assertIsInstance(t, TokenOpenBrace)

    def testLexCloseBrace(self):
        t = lex('{return 1;}')[4]
        self.assertIsInstance(t, TokenCloseBrace)

    def testLexAssign(self):
        t = lex('a=1')[1]
        self.assertIsInstance(t, TokenAssignmentOperator)

    def testLexEquality(self):
        t = lex('a==1')[1]
        self.assertIsInstance(t, TokenRelationalOperator)
        self.assertEqual(t.value, '==')

    def testLexSimpleMain(self):
        t = lex('int main() { int a=2; return a;}')
        expected = [
            'TokenKeyword int',
            'TokenIdentifier main',
            'TokenOpenParen (',
            'TokenCloseParen )',
            'TokenOpenBrace {',
            'TokenKeyword int',
            'TokenIdentifier a',
            'TokenAssignmentOperator =',
            'TokenInteger 2',
            'TokenSemicolon ;',
            'TokenKeyword return',
            'TokenIdentifier a',
            'TokenSemicolon ;',
            'TokenCloseBrace }',
        ]
        tks = [str(tk) for tk in t]
        self.assertEqual(tks, expected)

    def testLexSimpleMainWithLF(self):
        t = lex('int main() {\n  int a=2;\n  return a;\n}')
        expected = [
            'TokenKeyword int',
            'TokenIdentifier main',
            'TokenOpenParen (',
            'TokenCloseParen )',
            'TokenOpenBrace {',
            'TokenKeyword int',
            'TokenIdentifier a',
            'TokenAssignmentOperator =',
            'TokenInteger 2',
            'TokenSemicolon ;',
            'TokenKeyword return',
            'TokenIdentifier a',
            'TokenSemicolon ;',
            'TokenCloseBrace }',
        ]
        tks = [str(tk) for tk in t]
        self.assertEqual(tks, expected)

if __name__ == '__main__':
    unittest.main()
