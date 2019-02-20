#!/usr/bin/env python3

"""

    Sort the values of a list of columns.
    @Author: wavefancy@gmail.com

    Usage:
        SortColumns.py -s ints [-d string] [-c] [--cs txt]
        SortColumns.py -h | --help | -v | --version | --format | -f

    Options:
        -s ints    Sort the columns specified by ints, eg. 1|1,2,3, index starts from 1.
        -d string  Set the delimiter for fields. 'tab' for Tab.'\\t', default \\s+.
        -c         Open copy mode, directly copy comment line to stdout, comments started by '#'.
        --cs txt   Set the comment start string as 'txt', default it's '#'.

        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

    Notes:
        1. Read input from stdin, and output to stdout.
        2. Column index starts from 1.
"""

import sys
from docopt import docopt
import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def ShowFormat():
    sys.stderr.write('''
# INPUT
-------------------------------------------
#1 3 2
a b c
c b a

# OUTPUT: cat test.txt | python3 SortColumns.py -s 2,3 --cs '##'
-------------------------------------------
#1      2       3
a       b       c
c       a       b
    \n''')
    sys.stderr.close()
    sys.exit(-1)

def runApp():

    COMMENTS = args['--cs'] if args['--cs'] else '#'
    COPY_COMMENTS = True   if args['-c'] else False
    DELIMITER = args['-d'] if args['-c'] else None
    COLS = [int(x)-1 for x in args['-s'].split(',')]

    for line in sys.stdin:
        line = line.strip()
        if line:
            if COPY_COMMENTS:
                if line.startswith(COMMENTS):
                    sys.stdout.write('%s\n'%(line))
                    continue

            # start process non comment lines.
            ss = line.split(DELIMITER)
            COLS_V = [ss[x] for x in COLS]
            COLS_V = sorted(COLS_V)
            for x,y in zip(COLS, range(0,len(COLS))):
                ss[x] = COLS_V[y]

            sys.stdout.write('\t'.join(ss))
            sys.stdout.write('\n')

    sys.stdout.close()

if __name__ == '__main__':
    #check delimiter
    args = docopt(__doc__, version='1.0')
    # print(args)
    if args['--format']:
        ShowFormat()
        sys.exit(0)

    runApp()
