#!/usr/bin/env python3

"""

    Convert N lines to a single one line, repeat until file end.

    @Author: wavefancy@gmail.com

    Usage:
        N2OneLine.py -n int [-q text] [-d text] [-a]
        N2OneLine.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. See example by -f.

    Options:
        -n int        Convert the number of 'int' lines to a single line.
                          Any int >= 0. 0 means convert the whole file as a single line.
        -q text       Quote each input line element by 'text'.
        -d text       Set outpout delimiter for combined elements, default tab.
        -a            Append an extra '-d' delimiter value at each line end.
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
1
2
3
4
5

#output: -n 0
------------------------
1       2       3       4       5

#output: -n 2 -q "'"
------------------------
'1'     '2'
'3'     '4'
'5'

cat test.txt | python3 ./N2OneLine.py -n 3 -d ';'
------------------------
1;2;3
4;5
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    NUM_LINE = int(args['-n'])
    QUOTE    = args['-q'] if args['-q'] else ''
    OUT_DELIMITER = args['-d'] if args['-d'] else '\t'
    APPEND_D = True if args['-a'] else False

    out = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            if QUOTE:
                line = QUOTE + line + QUOTE

            if NUM_LINE == 0:
                out.append(line)
            else:
                out.append(line)
                if len(out) == NUM_LINE:
                    sys.stdout.write('%s'%(OUT_DELIMITER.join(out)))
                    if APPEND_D:
                        sys.stdout.write('%s\n'%(OUT_DELIMITER))
                    else:
                        sys.stdout.write('\n')
                    out = []

    #output the cached results in out.
    if out:
        sys.stdout.write('%s'%(OUT_DELIMITER.join(out)))
        if APPEND_D:
            sys.stdout.write('%s\n'%(OUT_DELIMITER))
        else:
            sys.stdout.write('\n')

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
