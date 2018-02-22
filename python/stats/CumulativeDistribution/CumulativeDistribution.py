#!/usr/bin/env python3

"""

    Estimate cumulative distribution.

    @Author: wavefancy@gmail.com

    Usage:
        CumulativeDistribution.py -c int [-n int] [-t] [-m]
        CumulativeDistribution.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output selected lines to stdout.
        2. Line index start from 1.

    Options:
        -c int        Column index for read data, single int or all.
                      All for estimate the CD for every column.
        -n int        Set the number of bins for estimating cumulative distribution, default 20.
        -m            Out put the count, rather than the proportion.
        -t            Set the first line as title, default False.
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
1 3
4 4
2 5
1 2
3 1
1 10

#output: -c 1 -n 5
------------------------
COL1    1.6000e+00      5.0000e-01
COL1    2.2000e+00      6.6667e-01
COL1    2.8000e+00      6.6667e-01
COL1    3.4000e+00      8.3333e-01
COL1    4.0000e+00      1.0000e+00

#output: -c all -n 5
------------------------
COL1    1.6000e+00      5.0000e-01
COL1    2.2000e+00      6.6667e-01
COL1    2.8000e+00      6.6667e-01
COL1    3.4000e+00      8.3333e-01
COL1    4.0000e+00      1.0000e+00
COL2    2.8000e+00      3.3333e-01
COL2    4.6000e+00      6.6667e-01
COL2    6.4000e+00      8.3333e-01
COL2    8.2000e+00      8.3333e-01
COL2    1.0000e+01      1.0000e+00
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    d_column = -1
    o_count = True if args['-m'] else False

    if args['-c']:
        if args['-c'].upper() == 'ALL':
            d_column = -100 # flag for estimate cd for every column.
        else:
            d_column = int(args['-c']) -1
    n_bins = 20;
    if args['-n']:
        n_bins = int(args['-n'])
    title = True if args['-t'] else False

    title_data = []
    # import scipy.stats as stats
    import numpy as np
    data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if title:
                title_data = ss
                title = False
                continue

            try:
                if d_column == -100: #for all columns.
                    data.append([float(x) for x in ss])
                else:
                    data.append([float(ss[d_column])])
            except ValueError:
                sys.stderr.write('ERROR: parse value error at line: %s\n'%(line))
                sys.exit(-1)

    #estimate frequency.
    for i in range(len(data[0])):
        inData = [x[i] for x in data]

        # cumfreqs, lowlim, binsize, extrapoints = stats.cumfreq(inData, numbins=n_bins)
        # evaluate the histogram
        values, base = np.histogram(inData, bins=n_bins)
        #evaluate the cumulative
        cumulative = np.cumsum(values)
        N = len(inData) * 1.0
        if o_count:
            cumfreqs = cumulative
        else:
            cumfreqs = cumulative/N
        #
        o_title = 'COL'+str(i+1)
        if title_data:
            o_title = title_data[i]
        #
        for i,v in zip(base[1:],cumfreqs):
            sys.stdout.write('%s\t%.4e\t%.4e\n'%(o_title,i,v))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
