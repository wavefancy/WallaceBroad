#!/usr/bin/env python

"""

    Calculate pvalue for Mann-Whitney U test. Call wilcox.test function from R by rpy2.
    @Author: wavefancy@gmail.com

    Usage:
        mannWhitneyUtestR.py [-a int]
        mannWhitneyUtestR.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout.
        2. Compute exact pvalue for small number of input.
        3. Output **One-sided p-value**.
        4. Detail R wilcox.test.

    Options:
        -a int        -1|0|1, Alternative test, default 0 for test two.sided.
                      -1 for less, 1 for greater.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''Input File format example:'''
    print('''
    #input example, each line two samples, separated by ';'
    ------------------------
0.80  0.83  1.89  1.04  1.45  1.38  1.91  1.64  0.73  1.46; 1.15  0.88  0.90  0.74  1.21

    #output example (benchmarked with R, wilcox.test)
    ------------------------
1.2721e-01
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    Alternative = 'two.sided'
    if args['-a'] == '-1':
        Alternative = 'less'
    elif args['-a'] == '1':
        Alternative = 'greater'

    # Call R function wilcox.test()
    from rpy2.robjects import FloatVector
    from rpy2.robjects.packages import importr
    stats = importr('stats')
    #http://rpy.sourceforge.net/rpy2/doc-dev/html/introduction.html
    def callRWilcoxTest(x,y):
        '''Call R function to do wilcox.test'''
        k = stats.wilcox_test(FloatVector(x),FloatVector(y),alternative=Alternative)
        return list(k[2])[0] # for pvalue.

    # data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split(';')
            try:
                # print(ss)
                x = [float(x) for x in ss[0].split() if x]
                y = [float(x) for x in ss[1].split() if x]

                sys.stdout.write('%s\n'%(callRWilcoxTest(x,y)))
            except ValueError:
                sys.stderr.write('WARNING: parse value error, skip one line: %s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
