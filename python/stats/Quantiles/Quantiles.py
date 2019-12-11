#!/usr/bin/env python

"""

    Compute and output quantiles from input list.
    @Author: wavefancy@gmail.com

    Usage:
        Quantiles.py -c <colindex> [-a float | -p <quantile>... | -r file]
        Quantiles.py -h | --help | -v | --version

    Notes:
        1. Read from stdin and output to stdout.

    Example:
        Quantiles.py -c 1 -p 0.1 0.95

    Options:
        -c            Column index for values. Starts from 1.
        -p            Output one or more quantiles, [0-1], based on the value distribution of '-c'.
        -a float      Compute the percentile of this value, based on the value distribution of '-c'.
        -r file       Read a file for a list of values to form a reference distribution, line by line.
                        And compute the percentile for each value in '-c' based
                        on the reference distribution.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.
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

    # Convert the values in '-c' to percentile based on the value distribution of '-c'
    from scipy.stats.mstats import mquantiles
    from scipy import stats
    if args['-r']:
        with open(args['-r'], 'r') as rdatafile:
            rdata = []
            for x in rdatafile.readlines():
                x = x.strip()
                if x:
                    x = x.split()
                    for y in x:
                        try:
                            rdata.append(float(y))
                        except:
                            sys.stderr.write('WARNING: parse float error, skip one value in reference '-r': %s\n'%(y))
            # print(rdata)
            # Convert each value to percentile based on distribution of values in '-r'
            for line in sys.stdin:
                line = line.strip()
                if line:
                    ss = line.split(None, P.maxSplit)
                    try:
                        t = float(ss[P.colIndex])
                        v = stats.percentileofscore(rdata,t)
                        # print(v)
                        ss.append('%g'%(v))
                    except:
                        ss.append('percentile')
                    sys.stdout.write('%s\n'%('\t'.join(ss)))

    # deal with flag -p and -a.
    else:
        data = []
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
                sys.stdout.write('%g\t%g\n'%(x,y))

        #quantitle for a particular score.
        if args['-a']:
            v = stats.percentileofscore(data,val)
            sys.stdout.write('%g\n'%(v))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
