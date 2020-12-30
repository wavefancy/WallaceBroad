#!/usr/bin/env python

"""

    Convert continuous variable to categorical, no covert on NA.

    @Author: wavefancy@gmail.com

    Usage:
        Continuous2Categorical.py -c name -n name (-b bins | -p bins) -l labels
        Continuous2Categorical.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout.
        2. Output results from stdout.
        3. Treat the first line as header.

    Options:
        -c name       Column name for the column to be converted.
        -n name       Column name for one column to be added for the labels.
        -b bins       Value bins for break continuous to categorical, eg 0,10,100.
                         The boundary are righ closed, (].
                         Values not in range will be set at NA.
                         the first m in the list represent min value -1.
                         the last  m in the list represent max value +1.
                         Using m can avoid calcuate min or max in advance.
        -p bins       Set the bin boundary by percentile in stead of actual values.
                        eg. m,0.3,m | 0.1,0.3,0.9
        -l labels     Labels for each categorical, eg. A,B. 
                         One label for each bin interval, so one element less than
                         the the bin boundary.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
#   Ref:
#        https://www.absentdata.com/pandas/pandas-cut-continuous-to-categorical/
#
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''Input File format example:'''
    print('''
#input example
------------------------
X
1
2
NA
3
4

# Test the range set as (], left open.
# cat test.txt | python3 ./Continuous2Categorical.py  -c X -n D -b 1,2,10 -l A,B
------------------------
X       D
1       NA
2       A
NA      NA
3       B
4       B

# Auto detect min or max.
# cat test.txt | python3 ./Continuous2Categorical.py  -c X -n M -b m,2,m -l A,B
------------------------
X       M
1       A
2       A
NA      NA
3       B
4       B

# Test using the percentile to specify cut-off.
# cat test.txt | python3 ./Continuous2Categorical.py  -c X -n M -p m,0.49,m -l A,B
X       M
1       A
2       A
NA      NA
3       B
4       B
    ''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    CNAME     = args['-c']
    newColumn = args['-n']
    labels =  args['-l'].split(',')


    import pandas as pd
    # Do not do auto conversion, will change the output number precision.
    data = pd.read_csv(sys.stdin,header=0,delim_whitespace=True,dtype=str)
    if CNAME not in data.columns:
        sys.stderr.write('ERROR: can not find column name in input header, key: %s\n'%(CNAME))
        sys.exit(-1)

    # data column used.
    dc = data[(CNAME)].astype(float)
    # print(dc)
    if args['-b']:
        bins     =  args['-b'].split(',')
    # Using percentile, convert the percentile to actual values.
    else:
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mstats.mquantiles.html
        from scipy.stats.mstats import mquantiles
        bins = []
        for v in args['-p'].split(','):
            if v == 'm':
                bins.append('m')
            else:
                bins.append(mquantiles(dc, prob = float(v))[0])

    bins[0]  =  bins[0]  if bins[0]  != 'm' else dc.min()-1.0
    bins[-1] =  bins[-1] if bins[-1] != 'm' else dc.max()+1.0
    # print(bins)
    # convert all number to numerical.
    bins   =  [float(x) for x in bins]
    cat_data = pd.cut(dc, bins=bins, labels=labels)

    # = pd.concat([data,cat_data], axis=1)
    data[newColumn] = cat_data
    data.to_csv(sys.stdout, sep='\t',index=False,na_rep='NA')

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
