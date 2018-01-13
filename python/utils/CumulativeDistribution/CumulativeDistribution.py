#!/usr/bin/env python3

"""

    Estimate cumulative distribution.

    @Author: wavefancy@gmail.com

    Usage:
        CumulativeDistribution.py -c int [-n int]
        CumulativeDistribution.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output selected lines to stdout.
        2. Line index start from 1.

    Options:
        -c int        Column index for read data.
        -n int        Set the number of bins for estimating cumulative distribution, default 20.
        -f file       Read line index from 'file', one line one index, load all in memory.
        -h --help     Show this screen.
        -v --version  Show version.

    Dependency:
        scipy

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
# input
------------------------
1
4
2
1
3
1

#output: -c 1 -n 5
------------------------
1.3750e+00      5.0000e-01
2.1250e+00      6.6667e-01
2.8750e+00      6.6667e-01
3.6250e+00      8.3333e-01
4.3750e+00      1.0000e+00
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    d_column = -1
    if args['-c']:
        d_column = int(args['-c']) -1
    n_bins = 20;
    if args['-n']:
        n_bins = int(args['-n'])

    import scipy.stats as stats
    data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                data.append(float(ss[d_column]))
            except ValueError:
                sys.stderr.write('WARN: parse value error at line: %s\n'%(line))

    #estimate frequency.
    cumfreqs, lowlim, binsize, extrapoints = stats.cumfreq(data, numbins=n_bins)
    # print(extrapoints)
    N = len(data) * 1.0
    for i,v in zip(range(len(cumfreqs)),cumfreqs):
        sys.stdout.write('%.4e\t%.4e\n'%(lowlim + (i+1)*binsize,v/N))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
