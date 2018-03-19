#!/usr/bin/env python3

"""

    Select rows by value range.

    @Author: wavefancy@gmail.com

    Usage:
        SelectByValueRange.py -c col -r range
        SelectByValueRange.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -c col         Column index for values, 1 based.
        -r range       Range threshold, both end included. eg: 1,5
                       M stands for min or max of the input values.
                       M,5: select from min to 5.
                       5,M: select from 5 to max.
        -h --help      Show this screen.
        -v --version   Show version.
        -f --format    Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def ShowFormat():
    '''Input File format example:'''
    print('''
# Input:
# ----------
1
2
m
3
4
5

# Output: -c 1 -r m,2
# ----------
1
2

# Output: -c 1 -r 3,4
# ----------
3
4
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    vcol = int(args['-c'])-1
    rr = args['-r'].lower().split(',')
    rr[0] = '-inf' if rr[0] == 'm' else rr[0]
    rr[1] = 'inf'  if rr[1] == 'm' else rr[1]
    rr = [float(x) for x in rr]

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                v = float(ss[vcol])
                if v>= rr[0] and v<=rr[1]:
                    sys.stdout.write('%s\n'%(line))

            except ValueError:
                sys.stderr.write('SKIPPED, parse value error: %s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
