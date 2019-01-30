#!/usr/bin/env python3

"""

    Transform the number of the first n columns to percentiles, percentile estimated
    from the n+1 to the end of this row.

    @Author: wavefancy@gmail.com

    Usage:
        PercentilesByRow.py -n ints [-m txt]
        PercentilesByRow.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output the transformed percentiles to stdout.
        2. See example by -f.
        3. The last column is the non-missing value count from the distribution
            to estimate the percentile.

    Options:
        -n ints        The first n columns to be transformed, index starts from 1.
        -m txt         Set the missing values, default NA.
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
#input
#--------------
1       1       2       3
2.5     1       2       3
N       NA      N       A
4       2       3       4
4       1       3       4

#output: -n 2
#--------------
0.0000  0.0000
50.0000 0.0000
PERCENTILE      PERCENTILE
100.0000        0.0000
100.0000        0.0000
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    N_COL = int(args['-n'])
    MISSING = args['-m'] if args['-m'] else 'NA'

    from scipy import stats
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                # vals = ss
                data = [x for x in ss[N_COL:] if x != MISSING]
                data = [float(x) for x in data]
                d    = [float(x) for x in ss[:N_COL]]

                out = [stats.percentileofscore(data,x) for x in d]
                out = ['%.4f'%(x) for x in out] + [str(len(data))]

                sys.stdout.write('%s\n'%("\t".join(out)))
            except Exception as e:
                sys.stdout.write('%s\n'%('\t'.join(["PERCENTILE"]*(N_COL+1))))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
