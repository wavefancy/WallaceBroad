#!/usr/bin/env python

"""

    Detect data outliters based on SD.

    @Author: wavefancy@gmail.com

    Usage:
        Outliers.py -c int -t float [--sl file]
        Outliers.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout.
        2. Output "outliters, beyond mean+/- t*sd" from stdout.

    Options:
        -c int        Column index for computing mean and sd value, 1 based.
        -t float      SD threshold for declearing as outliters, mean + [-t]*SD.
        --sl file     Line index for selecting records to estimate mean and sd, 1based.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
#   Ref:
#        1. https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
#
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''Input File format example:'''
    print('''
    ''');


if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    COL_INDEX = int(args['-c']) -1
    THRESHOLD = float(args['-t'])
    SELECTION = args['--sl'] if args['--sl'] else None
    SEL_SET   = None
    if SELECTION:
        SEL_SET = set()
        with open(SELECTION,'r') as infile:
            for line in infile:
                line = line.strip()
                if line:
                    SEL_SET.add(int(line)-1) # shift to 0 based.

    content = [] # [(value, line), (value, line),()....]
    values = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split(None, COL_INDEX +1)
            try:
                vv = float(ss[COL_INDEX])
                values.append(vv)
                content.append((vv, line))
            except ValueError:
                sys.stderr.write('Warnning: can not parse value from this line: "%s"\n'%(line))

    import numpy as np
    if SEL_SET:
        values = [v for k,v in enumerate(values) if k in SEL_SET]

    std = np.std(values)
    mean = np.mean(values)
    left = mean - THRESHOLD * std
    right = mean + THRESHOLD * std

    sys.stderr.write('Mean\tSTD\tLx*STD\tRx*STD\n')
    sys.stderr.write('%.4f\t%.4f\t%.4f\t%.4f\n'%(mean, std, left, right))

    for v,l in content:
        if v <= left or v >= right:
            sys.stdout.write('%s\n'%(l))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
