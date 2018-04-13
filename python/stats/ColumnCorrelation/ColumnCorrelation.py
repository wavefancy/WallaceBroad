#!/usr/bin/env python3

"""

    Compute column correlations by python pandas

    @Author: wavefancy@gmail.com

    Usage:
        ColumnCorrelation.py [-c int] [-r string]
        ColumnCorrelation.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output results to stdout.
        2. *** Treat first line as title line ***

    Options:
        -c int        Only calculate the correlation of this column with all the other columns.
        -r string     Set correlation name. pearson | kendall | spearman, default pearson.
        -h --help     Show this screen.
        -v --version  Show version.

    Dependency:
        pandas

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    corrName = 'pearson'
    corrSet = set(['pearson' , 'kendall' , 'spearman'])
    oneColumn = int(args['-c'])-1 if args['-c'] else -100
    # print(oneColumn)

    if args['-r']:
        if args['-r'] not in corrSet:
            sys.stderr.write('ERROR: option -r can only accept one of this: '+ str(corrSet))
            sys.exit(-1)
        else:
            corrName = args['-r']

    import pandas as pd
    df = pd.read_csv(sys.stdin, sep='\s+')
    if oneColumn>=0:
        # print(oneColumn)
        names = df.columns
        oname1 = names[oneColumn]
        for i in names:
            if i != oname1:
                re = df[oname1].corr(df[i],method=corrName)
                sys.stdout.write('%s\t%s\t%.4e\n'%(oname1,i,re))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
