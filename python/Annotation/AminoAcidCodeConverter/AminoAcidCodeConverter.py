#!/usr/bin/env python3

"""

    Convert the amino acid coding scheme between 3 or 1 letters.

    @Author: wavefancy@gmail.com

    Usage:
        AminoAcidCodeConverter.py -c int [--13] [-t]
        AminoAcidCodeConverter.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output results to stdout.
            Add one more column for the convertion.

    Options:
        -c int        The column to do the convertion.
        --13          Convert from 1 letter to 3 letters, default 3 to 1.
        -t            Indicate the first line as title, no convertion.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
import re
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
A11D    ALA11ASP
R17T    ARG17THR

#output: -c 1 --13
#-----------------------------
A11D    ALA11ASP        ALA11ASP
R17T    ARG17THR        ARG17THR

#output: -c 2
#-----------------------------
A11D    ALA11ASP        A11D
R17T    ARG17THR        R17T
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    COL = int(args['-c'])-1
    NO_TITLE  = False if args['-t'] else True
    CONVERT31 = False if args['--13'] else True
    # https://stackoverflow.com/questions/12760271/how-do-i-convert-the-three-letter-amino-acid-codes-to-one-letter-code-with-pytho
    # http://www.fao.org/3/y2775e/y2775e0e.htm
    # http://www.hgvs.org/mutnomen/references.html
    d31 = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
     'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
     'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
     'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}
    d13 = {y:x for x,y in d31.items()}

    def convert31(code):
        """Convert from 3 letters to 1"""
        code = code.upper()
        c1 = code[:3]
        c2 = code[-3:]
        return d31[c1] + code[3:-3] + d31[c2]

    def convert13(code):
        ''''Convert from 1 letter to 3 letters'''
        code = code.upper()
        c1 = code[:1]
        c2 = code[-1:]
        return d13[c1] + code[1:-1] + d13[c2]

    for line in sys.stdin:
        line = line.strip()
        if line:
            if NO_TITLE:
                ss = line.split()
                if CONVERT31:
                    sys.stdout.write('%s\t%s\n'%(line,convert31(ss[COL])))
                else:
                    sys.stdout.write('%s\t%s\n'%(line,convert13(ss[COL])))
            else:
                sys.stdout.write('%s\n'(line))
                NO_TITLE = True

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
