#!/usr/bin/env python3

"""

    Transform the number of a column to percentiles.
    @Author: wavefancy@gmail.com

    Usage:
        Percentiles.py -c col
        Percentiles.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout add one more column for percentiles.
        2. See example by -f.

    Options:
        -c col         Column index for transformer to be applied.
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
c1 2
c2 2
c3 NA
C4 4

#output
#--------------
c1      2       5.0000e-01
c2      2       5.0000e-01
c3      NA      PERCENTILE
C4      4       1.0000e+00
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    COL = int(args['-c']) -1

    import scipy.stats.mstats as ms
    # ms.rankdata, If some values are tied, their rank is averaged.
    #[1,1,2, 7 ,2,4] -> [1.5, 1.5, 3.5, 6. , 3.5, 5. ]

    data = []
    OK_Data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                val = float(ss[COL])
                OK_Data.append(val)
                data.append(ss+[val])
            except Exception as e:
                data.append(ss+['PERCENTILE'])

    # transform data to percentile
    OK_Data = ms.rankdata(OK_Data)/len(OK_Data)

    #output results
    index = 0
    for d in data:
        if d[-1] != 'PERCENTILE':
            d[-1] = '%.4e'%(OK_Data[index])
            index +=1

        sys.stdout.write('%s\n'%('\t'.join(d)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
