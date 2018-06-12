#!/usr/bin/env python3

"""

    Selection damaging prediction from several algorithms.

    @Author: wavefancy@gmail.com

    Usage:
        DamagingSelector.py -c text (-n int | -a)
        DamagingSelector.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output results to stdout.
        2. Line starts with '#' will be copy to stdout directly, useful for title.
        3. Count the number of algorithms with damaging predction, and output the
            records meet the threshold (>=).

    Options:
        -c text       Column index for the algorithm prediction(1 based), eg. 1|1,2,3.
        -n int        Threshold for the number of damaging prediction.
        -a            Annotate the number of damaging prediction, no selection.
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
#-------------------
#Title
x1 D    P
x2 N    D
x3 p    p

#output: -c 2,3 -n 2
#-------------------
#Title
x1 D    P
x3 p    p

#output: -c 2,3 -a
#-------------------
#Title  #Damaging
x1 D    P       2
x2 N    D       1
x3 p    p       2
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    cols = [int(x)-1 for x in args['-c'].split(',')]
    threshold = int(args['-n']) if args['-n'] else None
    annotate = True if args['-a'] else False
    damaging = set(['D','P'])

    for line in sys.stdin:
        line = line.strip()
        if line:
            if line.startswith('#'):
                if annotate:
                    sys.stdout.write('%s\t#Damaging\n'%(line))
                    continue
                else:
                    sys.stdout.write('%s\n'%(line))
                    continue

            ss = line.split()
            predictions = [ss[x].upper() for x in cols]
            c = len([x for x in predictions if x in damaging])
            if annotate:
                sys.stdout.write('%s\t%d\n'%(line,c))
            else:
                if c >= threshold:
                    sys.stdout.write('%s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
