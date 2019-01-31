#!/usr/bin/env python3

"""

    Transform the number of the first n columns to percentiles, percentile estimated
    from the n+1 to the end of this row.

    @Author: wavefancy@gmail.com

    Usage:
        PercentilesByRow.py -n int
        PercentilesByRow.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output the transformed percentiles to stdout.
        2. See example by -f.

    Options:
        -n ints        The first n columns to be transformed, index starts from 1.
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

    from scipy import stats
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                vals = [float(x) for x in ss]

                data = vals[N_COL:]
                out = [stats.percentileofscore(data,x) for x in vals[:N_COL]]
                out = ['%.4f'%(x) for x in out]

                sys.stdout.write('%s\n'%("\t".join(out)))
            except Exception as e:
                sys.stdout.write('%s\n'%('\t'.join(["PERCENTILE"]*N_COL)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
