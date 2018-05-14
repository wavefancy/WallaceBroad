#!/usr/bin/env python3

"""

    Transpose an input text file(matrix).

    @Author: wavefancy@gmail.com

    Usage:
        Transpose.py
        Transpose.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. ***Input file each line should have the number fields.****
        3. See example by -f.

    Options:
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    #input:
    ------------------------
1   2   3
4   5   6

    #output:
    ------------------------
1       4
2       5
3       6
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    #load all data into memory.
    data = [line.strip().split() for line in sys.stdin if line.strip()]
    # check the number of fields for each line.
    for v in data[1:]:
        if len(v) != len(data[0]):
            sys.stderr.write('ERROR: Not all the input lines have the same number of fields.\n')
            sys.exit(-1)

    #Transpose data and output.
    for line in zip(*data):
        sys.stdout.write('%s\n'%('\t'.join(line)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
