#!/usr/bin/env python3

"""

    Partition the data into bins according to a column of value.

    @Author: wavefancy@gmail.com

    Usage:
        MakeBins.py -c col -n int (--es | --en)
        MakeBins.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
            add one more column for bin group label.
        2. See example by -f.

    Options:
        -c col         Column index for the data to group into bins.
        -n int         The number of bins.
        --es           Partition the bins as equal value steps, pandas.cut.
        --en           Partition the bins as equal number of values in each bin, pandas.qcut.
        -h --help      Show this screen.
        -v --version   Show version.
        -f --format    Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
import pandas
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def ShowFormat():
    '''Input File format example:'''
    print('''
#input
#--------------
0   1
1   2
2   N
3   4
5   10
x   60

#MakeBins.py -c 2 -n 3 --es
#--------------
0       1       0
1       2       0
2       N       NA
3       4       0
5       10      0
x       60      2

#MakeBins.py -c 2 -n 3 --en
#--------------
0       1       0
1       2       0
2       N       NA
3       4       1
5       10      2
x       60      2
    ''');

# https://stackoverflow.com/questions/30211923/what-is-the-difference-between-pandas-qcut-and-pandas-cut
# cut will choose the bins to be evenly spaced according to the values themselves and not the frequency of those values.
# qcut, the bins will be chosen so that you have the same number of records in each bin.
# qcut api:
# https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.qcut.html
# cut api:
# https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.cut.html

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    COL =  int(args['-c']) -1
    NBINS =int(args['-n'])

    data = []
    COL_Data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            data.append(ss)
            try:
                val = float(ss[COL])
                COL_Data.append(val)
            except Exception as e:
                COL_Data.append(None)

    OK_Data = [x for x in COL_Data if x]
    if args['--en']:
        labels = pandas.qcut(OK_Data, NBINS, labels=False)
    elif args['--es']:
        labels = pandas.cut(OK_Data, bins=NBINS, labels=False)

    index = 0
    labels = [str(x) for x in labels]
    for d,c in zip(data, COL_Data):
        out = []
        if c:
            out = d + [labels[index]]
            index+=1
        else:
            out = d + ['NA']
        # print(out)
        sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
