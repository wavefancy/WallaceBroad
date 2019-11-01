#!/usr/bin/env python3

"""
    Rank based inverse normal transformation.
        During INT, the sample measurements are first mapped to the probability scale,
        by replacing the observed values with fractional ranks,
        then transformed into Z-scores using the probit function
    More details:
        https://cran.rstudio.com/web/packages/RNOmni/vignettes/RNOmni.html

    @Author: wavefancy@gmail.com

    Usage:
        InverseNormalTransformation.py -c txt [-d]
        InverseNormalTransformation.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read pandas dataframe from stdin, and output results to stdout,
        2. See example by -f.

    Options:
        -c txt         The column name for the column to be transformed.
        -d             Drop the original value, only keep the transformed values.
        -h --help      Show this screen.
        -v --version   Show version.
        -f --format    Show input/output file format example.
"""
import sys
from docopt import docopt
import pandas as pd
import numpy as np
import scipy.stats as ss
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def ShowFormat():
    '''Input File format example:'''
    print('''
#example input
-----------------------------
A B C
a 1 1
b 2 2
c 2 NA
d 3 4

# cat test.txt | python3 ./InverseNormalTransformation.py  -c B
-----------------------------
A       B       C       B_INV
a       1       1       -1.15035
b       2       2       -0.318639
c       2       NA      0.318639
d       3       4       1.15035
    ''');

# code base from:
# https://github.com/edm1/rank-based-INT/blob/master/rank_based_inverse_normal_transformation.py

def rank_INT(series, c=3.0/8, stochastic=True):
    """ Perform rank-based inverse normal transformation on pandas series.
        If stochastic is True ties are given rank randomly, otherwise ties will
        share the same value. NaN values are ignored.
        Args:
            param1 (pandas.Series):   Series of values to transform
            param2 (Optional[float]): Constand parameter (Bloms constant)
            param3 (Optional[bool]):  Whether to randomise rank of ties

        Returns:
            pandas.Series
    """

    # Check input
    assert(isinstance(series, pd.Series))
    assert(isinstance(c, float))
    assert(isinstance(stochastic, bool))

    # Set seed
    np.random.seed(123)

    # Take original series indexes
    orig_idx = series.index

    # check isnull.
    # print(series.loc[pd.isnull(series)])
    if len(series.loc[pd.isnull(series)]) > 0:
        sys.stderr.write('ERROR: We can not transform NA values, please remove them.\n')
        sys.exit(-1)

    # Drop NaNs
    series = series.loc[~pd.isnull(series)]

    # Get ranks
    if stochastic == True:
        # Shuffle by index
        series = series.loc[np.random.permutation(series.index)]
        # Get rank, ties are determined by their position in the series (hence
        # why we randomised the series)
        rank = ss.rankdata(series, method="ordinal")
    else:
        # Get rank, ties are averaged
        # https://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.stats.rankdata.html
        rank = ss.rankdata(series, method="average")

    # Convert numpy array back to series
    rank = pd.Series(rank, index=series.index)

    # Convert rank to normal distribution
    transformed = rank.apply(rank_to_normal, c=c, n=len(rank))

    return transformed[orig_idx]

def rank_to_normal(rank, c, n):
    # Standard quantile function
    x = (rank - c) / (n - 2*c + 1)
    return ss.norm.ppf(x)

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    data = pd.read_csv(sys.stdin,header=0,delim_whitespace=True)
    cname = args['-c']
    if cname not in data.columns.values:
        sys.stderr.write('ERROR: Can not find column name: %s\n'%(cname))
        sys.exit(-1)

    # print(type(data[cname]))
    ivt_data = rank_INT(data[cname], 0.5, True)
    if args['-d']:
        data[cname] = ivt_data
    else:
        data[cname+'_INV'] = ivt_data

    data.to_csv(sys.stdout, sep='\t',index=False,float_format='%g',na_rep='NA')

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
