#!/usr/bin/env python

"""

    Convert categorical data to dummy variable. NA are ignored.

    @Author: wavefancy@gmail.com

    Usage:
        Categorical2Dummy.py -n name [-k] [--nd]
        Categorical2Dummy.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout.
        2. Output results from stdout.
        3. Treat the first line as header.

    Options:
        -n name       Column name for the column to be converted.
        -k            Keep the column which was converted. Default: Skip.
        --nd          Do not drop the first categoricy.
                         Default drop the first to avoid multicollinearity.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
#   Ref:
#        1. https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
#
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''Input File format example:'''
    print('''
#input example
------------------------
X1      C
1       C1
2       C2
3       C1
4       C3
5       C2
6       C2

#cat test.txt |  cat test.txt | python3 Categorical2Dummy.py -n C -k --nd
------------------------
X1      C       C_C1    C_C2    C_C3
1       C1      1       0       0
2       C2      0       1       0
3       C1      1       0       0
4       C3      0       0       1
5       C2      0       1       0
6       C2      0       1       0
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    CNAME = args['-n']
    KEEP  = True if args['-k'] else False
    drop_first = False if args['--nd'] else True
    import pandas as pd

    data = pd.read_csv(sys.stdin,header=0,delim_whitespace=True)
    if CNAME not in data.columns:
        sys.stderr.write('ERROR: can not find column name in input header, key: %s\n'%(CNAME))
        sys.exit(-1)

    dummy = pd.get_dummies(data[(CNAME)],prefix=CNAME, drop_first = drop_first)
    if not KEEP:
        cols = [x for x in data.columns if x != CNAME]
        data = data[cols]

    results = pd.concat([data,dummy], axis=1)
    results.to_csv(sys.stdout, sep='\t',index=False,na_rep='NA')

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
