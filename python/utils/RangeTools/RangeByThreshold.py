#!/usr/bin/env python3

"""

    Select range by threshold.

    @Author: wavefancy@gmail.com

    Usage:
        RangeByThreshold.py -p int -c int -t float [-e int] [-s]
        RangeByThreshold.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output ranges to stdout.
        2. Column index start from 1.
        3. *** important *** input should sorted by position.

    Options:
        -p int        Column index for position, 1 based.
        -c int        Column index for value.
        -t float      Threshold for comparion.
        -s            Default is a value >= threshold will be included,
                      If this option is on, value <= threshold will be included.
        -e int        Extend the selected range by this value, default 2000000.
        -f --format   Show example.       
        -h --help     Show this screen.
        -v --version  Show version.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def ShowFormat():
    print('''
# input
#-----------------
100     10
1000000 20
5000000 20
7000000 3
10000000 30

# cat in.txt | python3 RangeByThreshold.py -p 1 -c 2 -t 20
#-----------------
-1000000        7000000
8000000 12000000
    ''')

if __name__ == '__main__':
    args = docopt(__doc__, version='3.0')
    #print(args)

    if(args['--format'] or args['-f']):
        ShowFormat()
        sys.exit(-1)
#

    colPos = int(args['-p']) -1
    colValue  = int(args['-c']) -1
    threshold = float(args['-t'])
    extend = 2000000
    if args['-e']:
        extend = int(args['-e'])

    big = True
    if args['-s']:
        big = False

#-------------------------------------------------
    start = ''
    end = ''
    last = 0 #cached last location.
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                p = int(ss[colPos])
                v = int(ss[colValue])

                if big:
                    if v >= threshold:
                        if not start:
                            start = p
                    else:
                        if start:
                            sys.stdout.write('%d\t%d\n'%(start - extend, last + extend))
                            start = ''
                last = p #update the last location.

            except ValueError:
                sys.stderr.write('WARN: parse value error(skiped): %s\n'%(line))

    #check for the last location
    if start:
        sys.stdout.write('%d\t%d\n'%(start - extend, last + extend))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
