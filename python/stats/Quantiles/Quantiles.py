#!/usr/bin/env python

"""

    Compute and output quantiles from input list.
    @Author: wavefancy@gmail.com

    Usage:
        Quantiles.py -c <colindex> [-a float | -p <quantile>...]
        Quantiles.py -h | --help | -v | --version

    Notes:
        1. Read from stdin and output to stdout.

    Example:
        Quantiles.py -c 1 -p 0.1 0.95

    Options:
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.
        -c            Column index for values. Starts from 1.
        -p            One or more quantiles, [0-1].
        -a float      Compute the percentile of this value.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

class P(object):
    colIndex = -1
    quantitle = []
    maxSplit = -1

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)

    P.colIndex = int(args['<colindex>']) -1 # shift to 0 based.
    P.maxSplit = P.colIndex + 2

    P.quantitle = list(map(float, args['<quantile>']))
    # print(P.quantitle)
    #check quantitle range.
    for x in P.quantitle:
        if x < 0 or x > 1:
            sys.stderr.write('ERROR: Quantitle should be in [0-1], your input: %s\n'%(str(P.quantitle)))
            sys.exit(-1)
    val = float(args['-a']) if args['-a'] else ''

    data = []
    from scipy.stats.mstats import mquantiles
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split(None, P.maxSplit)
            try:
                data.append(float(ss[P.colIndex]))
            except:
                sys.stderr.write('WARNING: skip one line: %s\n'%(line))

    if args['-p']:
        qq = mquantiles(data, prob = P.quantitle)
        sys.stdout.write('Quantile\tValue\n')
        for x,y in zip(P.quantitle, qq):
            sys.stdout.write('%f\t%.4e\n'%(x,y))

    #quantitle for a particular score.
    if args['-a']:
        from scipy import stats
        v = stats.percentileofscore(data,val)
        sys.stdout.write('%.6f\n'%(v))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
