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
