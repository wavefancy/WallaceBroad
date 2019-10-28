#!/usr/bin/env python3

'''

    Merge successive columns into one column.

    @Author: wavefancy@gmail.com, Wallace Wang.

    Usage:
        MergeColumns.py -c ints [-t txt] [-d txt]
        MergeColumns.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.

    Options:
        -c ints       Successive columns to merge together. eg. 1-2|2-4.
                        Both ends included.
        -d txt        The delimiter for merged columns, default ':'.
        -t text       The title for the new insertting column(s).
        -h --help     Show this screen.
        --version     Show version.
        -f --format   Show input/output file format example.

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.
from docopt import docopt

def ShowFormat():
    '''File format example'''
    print('''
#Input file format(stdin)
#------------------------
1       t1      t2      2
1       0       0       2

#Output:
#cat test.txt | python3 ./MergeColumns.py  -c 2-3 -t title
#------------------------
1       title   2
1       0:0     2
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    ENDS    = [int(x)-1 for x in args['-c'].split('-')] #shift to 0 based.
    ENDS[1] += 1 # make both ends included.
    TITLE   = args['-t'] if args['-t'] else ''
    delimiter = args['-d'] if args['-d'] else ':'
    # print(ENDS)

    for line in sys.stdin:
        line = line.strip()
        if line :
            ss = line.split()
            L    = ss[:ENDS[0]]
            M    = [delimiter.join(ss[ENDS[0]:ENDS[1]])]
            R    = ss[ENDS[1]:]
            # print(ss)
            if TITLE:
                out = L + [TITLE] + R
                TITLE = None
            else:
                out = L + M + R

            sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
