import os
import sys
import lexer
import parser
import codegen

if __name__ == '__main__':
    source_file = sys.argv[1]
    assembly_file = os.path.splitext(source_file)[0] + '.s'

    with open(source_file, 'r') as infile, open(assembly_file, 'w') as outfile:
        source = infile.read().strip()
        assembly = codegen(parse(tokenize(source)))
        outfile.write(str(assembly))
