#!/usr/bin/env python3

"""

    Using numpy compute the column mean.

    @Author: wavefancy@gmail.com

    Usage:
        ColumnStreamMean.py
        ColumnStreamMean.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data with header from stdin.
        2. Default code the missing data 'nan'.
        3. Output results to stdout.

    Options:
        -h --help       Show this screen.
        -v --version    Show version.
        -f --format     Show format example.
"""
import sys
from docopt import docopt
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
#----------------
A       B       C
1       nan     3
0       1       3
1       2       4
#----------------
STATS   A       B       C
MEAN    0.66666667      1.5             3.33333333
COUNTS  3       2       3
    ''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)
    
    MISS = 'nan'
    SEP  = '\t'

    data_sum = []
    data_count = []
    TITLE = False
    for line in sys.stdin:
        if not TITLE:
            sys.stdout.write('STATS\t'+line)
            l = len(line.strip().split())
            data_sum   = np.zeros(l)
            data_count = np.zeros(l,dtype=int)
            TITLE = True
        else:
            i = np.fromstring(line,sep=SEP)
            # print(i)
            is_miss = np.isnan(i)
            # non-missing as 1, missing as 0.
            i_count = np.logical_not(is_miss).astype(int)
            data_count += i_count
            # mask missing as 0.
            i[is_miss] = 0
            data_sum   += i
    
    # print(data_sum)
    # print(data_count)
    #output the results.
    np.set_printoptions(threshold=sys.maxsize,linewidth=sys.maxsize)
    sys.stdout.write('MEAN\t'+np.array2string(data_sum/data_count,separator='\t')[1:-1])
    sys.stdout.write('\nCOUNTS\t'+np.array2string(data_count,separator='\t')[1:-1])
    sys.stdout.write('\n')

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
