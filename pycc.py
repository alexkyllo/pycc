import os
import sys
import re

def tokenize(input):
    token_definitions = (
        ('keyword_int', 'int'),
        ('keyword_return','return'),
        ('open_brace', '{'),
        ('close_brace', '}'),
        ('open_paren', '\('),
        ('close_paren', '\)'),
        ('semicolon', ';'),
        ('identifier', '[a-zA-Z_][a-zA-Z0-9_]*'),
        ('integer', '[0-9]+'),
        #('double', '[0-9]*\.?[0-9]+.')
    )

    tokens = []

    input_string = input

    while len(input_string) > 0:
        for tokdef in token_definitions:
            print(input_string)
            regex_string = tokdef[1]
            print(regex_string)

            regex = re.compile(regex_string)
            match_result = regex.match(input_string)
            if match_result:
                print("matched {0}".format(match_result.group()))
                tokens.append((tokdef[0], match_result.group()))
                end = match_result.end()
                break
            else:
                end = 1
        input_string = input_string[end:]

    return tokens


def parse(tokens):
    return tokens

def compile(ast):
    return ast

if __name__ == '__main__':
    source_file = sys.argv[1]
    assembly_file = os.path.splitext(source_file)[0] + '.s'

    with open(source_file, 'r') as infile, open(assembly_file, 'w') as outfile:
        source = infile.read().strip()
        assembly = compile(parse(tokenize(source)))
        outfile.write(str(assembly))
