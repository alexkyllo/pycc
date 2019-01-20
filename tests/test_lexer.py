import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from pycc import tokenize

class TestLexer(unittest.TestCase):

    def testLexInt(self):
        t = tokenize('int')[0]
        assert(t == ('keyword_int', 'int'))

    def testLexReturn(self):
        t = tokenize('return 2;')[0]
        assert(t == ('keyword_return', 'return'))

    def testLexDouble(self):
        t = tokenize('return 1.234;')[1]
        assert(t == ('double', '1.234'))

    def testLexOpenBrace(self):
        t = tokenize('{return 1;}')[0]
        assert(t == ('open_brace', '{'))

    def testLexCloseBrace(self):
        t = tokenize('{return 1;}')[4]
        assert(t == ('close_brace', '}'))

    def testLexAssign(self):
        t = tokenize('a=1')[1]
        assert(t == ('assignment', '='))

    def testLexEquality(self):
        t = tokenize('a==1')[1]
        assert(t == ('equality', '=='))

    def testLexSimpleMain(self):
        t = tokenize('int main() {return 2;}')
        expected = [
            ('keyword_int', 'int'),
            ('identifier', 'main'),
            ('open_paren', '('),
            ('close_paren', ')'),
            ('open_brace', '{'),
            ('keyword_return', 'return'),
            ('integer', '2'),
            ('semicolon', ';'),
            ('close_brace', '}')
        ]
        self.assertEqual(t, expected)

    def testLexSimpleMainWithLF(self):
        t = tokenize('int main() {\n  return 2;\n}')
        expected = [
            ('keyword_int', 'int'),
            ('identifier', 'main'),
            ('open_paren', '('),
            ('close_paren', ')'),
            ('open_brace', '{'),
            ('keyword_return', 'return'),
            ('integer', '2'),
            ('semicolon', ';'),
            ('close_brace', '}')
        ]
        self.assertEqual(t, expected)

if __name__ == '__main__':
    unittest.main()
