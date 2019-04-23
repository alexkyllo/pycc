import os
import sys
import re

class Token():
    def __init__(self, pattern, value=None):
        self.pattern = re.compile(pattern)
        if value:
            self.lex(str(value))
        else:
            value = None

    def lex(self, string):
        matched = self.pattern.match(string)
        if matched:
            self.value = matched.group()
            self.start = matched.start()
            self.end = matched.end()
        else:
            self.value = None
            self.start = None
            self.end = None

    def __str__(self):
        return "{0} {1}".format(self.__class__.__name__, self.value)

class TokenKeyword(Token):
    def __init__(self, value=None):
        super().__init__(
            (
            "auto|break|case|char|const|continue|default|do|"
            "double|else|enum|extern|float|for|goto|if|int|"
            "long|register|return|short|signed|sizeof|static|"
            "struct|switch|typedef|union|unsigned|void|volatile|while"
            ),
            value
        )

class TokenOpenBrace(Token):
    def __init__(self, value='{'):
        super().__init__('{', value)

class TokenCloseBrace(Token):
    def __init__(self, value='}'):
        super().__init__('}', value)

class TokenOpenParen(Token):
    def __init__(self, value='\('):
        super().__init__('\(', value)

class TokenCloseParen(Token):
    def __init__(self, value='\)'):
        super().__init__('\)', value)

class TokenSemicolon(Token):
    def __init__(self, value=';'):
        super().__init__(';', value)

class TokenAssignmentOperator(Token):
    def __init__(self, value=None):
        super().__init__('[<]{2}=|[>]{2}=|[\+\-\*\/%\&\^\!\|]?[=](?!=)', value)

class TokenAdditionOperator(Token):
    def __init__(self, value=None):
        super().__init__('[\+\-]', value)

class TokenMultiplicationOperator(Token):
    def __init__(self, value=None):
        super().__init__('[\*\/%]', value)

class TokenIncrementOperator(Token):
    def __init__(self, value=None):
        super().__init__('[+]{2}|[-]{2}', value)

class TokenEqualityOperator(Token):
    def __init__(self, value=None):
        super().__init__('[=\!][=]', value)

class TokenInequalityOperator(Token):
    def __init__(self, value=None):
        super().__init__('[\>\<][=]|[<>]', value)

class TokenLogicalOperator(Token):
    def __init__(self, value=None):
        super().__init__('&{2}|\|{2}|\!(?!=)', value)

class TokenIdentifier(Token):
    def __init__(self, value=None):
        super().__init__('[a-zA-Z_][a-zA-Z0-9_]*', value)

class TokenInteger(Token):
    def __init__(self, value=None):
        super().__init__('[0-9]+(?!\.)', value)

    def lex(self, string):
        super().lex(string)
        if self.value:
            self.value = int(self.value)

class TokenFloat(Token):
    def __init__(self, value=None):
        super().__init__('[0-9]*\.?[0-9]+', value)

    def lex(self, string):
        super().lex(string)
        if self.value:
            self.value = float(self.value)

class TokenString(Token):
    def __init__(self, value=None):
        super().__init__('"\w+"', value)

def lex(input_string):
    token_types = (
        TokenKeyword,
        TokenOpenBrace,
        TokenCloseBrace,
        TokenOpenParen,
        TokenCloseParen,
        TokenSemicolon,
        TokenAssignmentOperator,
        TokenAdditionOperator,
        TokenMultiplicationOperator,
        TokenEqualityOperator,
        TokenInequalityOperator,
        TokenLogicalOperator,
        TokenIdentifier,
        TokenInteger,
        TokenFloat,
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
