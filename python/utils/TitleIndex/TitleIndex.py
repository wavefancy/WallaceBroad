#!/usr/bin/env python3

"""

    Add index number for title line

    @Author: wavefancy@gmail.com

    Usage:
        TitleIndex.py [-0] [-c]
        TitleIndex.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. ***Input file each line should have the number fields.****
        3. See example by -f.

    Options:
        -0            Index as 0 based. Default 1 based.
        -c            Skip comment line, comment line start as #(default).
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
#A B
1 2

#output:
------------------------
#A:1    B:2
1 2

#output: -0
------------------------
#A:0    B:1
1 2

#output: -0 -c
------------------------
#A B
1:0     2:1
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    INDEX_START = 0 if args['-0'] else 1
    SKIP_COMMENT = True if args['-c'] else False
    COMMENT_START = '#'

    INDATA = False
    for line in sys.stdin:
        if INDATA:
            sys.stdout.write(line)
        elif SKIP_COMMENT and line.startswith('#'):
            sys.stdout.write(line)
        else:
            INDATA = True
            ss = line.strip().split()
            out = []
            for i, x in enumerate(ss,INDEX_START):
                out.append(x+':'+str(i))

            sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
