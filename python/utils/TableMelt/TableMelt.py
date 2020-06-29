#!/usr/bin/env python3

'''

    Reshape the input data by pandas.melt
    # https://towardsdatascience.com/reshape-pandas-dataframe-with-melt-in-python-tutorial-and-visualization-29ec1450bb02

    @Author: wavefancy@gmail.com, Wallace Wang.

    Usage:
        TableMelt.py [-d delimiter] --id txt --var txt --val txt
        TableMelt.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.

    Options:
        -d delimiter  Set title delimiter, default \s+.
        --id txt      The id_var for table melt.
        --var txt     The var_name for table melt.
        --val txt     The value_name for table melt.
        -h --help     Show this screen.
        --version     Show version.
        -f --format   Show input/output file format example.

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.
from docopt import docopt
import pandas as pd

def ShowFormat():
    '''File format example'''
    print('''
# INPUT
-------------------
A B C
1 2 3
4 5 6

#cat in.test.txt | python3 ./TableMelt.py --id A --var Title --val VALUE
------------------------
A       Title   VALUE
1       B       2
4       B       5
1       C       3
4       C       6
          ''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    DELIMITER = args['-d'] if args['-d'] else r'\s+'
    ID = args['--id']
    VAR_NAME = args['--var']
    VALUE_NAME = args['--val']

    data = pd.read_csv(sys.stdin,header=0,delimiter=DELIMITER, dtype='str')
    out = pd.melt(frame=data,id_vars=ID,var_name=VAR_NAME,value_name=VALUE_NAME)
    out.to_csv(sys.stdout, index=False)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
