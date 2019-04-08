#!/usr/bin/env python3

"""

    Two sample t-test by scipy library.

    @Author: wavefancy@gmail.com

    Usage:
        TTest.py [-l] [-e]
        TTest.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output selected lines to stdout.
        2. Output format, [GropName] PValue t-statistic.

    Options:
        -l            Set the input data has label.
        -e            Set equal variance of two samples, default unequal variance.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
# input example: -l
--------------------------
t1 1 2 3 4;t2 6 7 8 9 10

# input example:
--------------------------
1 2 3 4;6 7 8 9 10
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    LABEL = False
    equalVar = False

    title=['PVALUE','T_STATISTICS']
    if args['-l']:
        LABEL = True
        title = ['GROUP_NAME1','GROUP_NAME2'] + title
    if args['-e']:
        equalVar = True
    sys.stdout.write('%s\n'%('\t'.join(title)))
#-------------------------------------------------
    from scipy import stats
    for line in sys.stdin:
        line = line.strip()
        if line:
            gg = line.split(';')

            d1 = gg[0].strip().split()
            d2 = gg[1].strip().split()
            t1 = ''
            t2 = ''
            if LABEL:
                t1 = d1[0].strip()
                t2 = d2[0].strip()
                d1 = d1[1:]
                d2 = d2[1:]

            d1 = [float(x) for x in d1]
            d2 = [float(x) for x in d2]

            r = stats.ttest_ind(d1, d2, equal_var = equalVar)

            out = ''
            if t1:
                out = out + t1 + '\t' + t2 + '\t'

            out += '%.4e'%(r[1]) + '\t'
            out += '%.4e'%(r[0])

            sys.stdout.write('%s\n'%(out))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
