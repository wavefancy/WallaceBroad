#!/usr/bin/env python

"""

    Perform multiple linear regression, Y ~ X1 + X2 + ... Xn
    @Author: wavefancy@gmail.com

    Usage:
        MultipleLinearRegression.py [-t] [-n]
        MultipleLinearRegression.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout. Y, X1, X2, each variable one line.
        2. Output results from stdout.

    Options:
        -t            Indicate first column as title, default False.
        -n            Apply z-score noramlization of the input data, default False.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
#   Ref:
#        1. https://stackoverflow.com/questions/11479064/multiple-linear-regression-in-python
#        2. https://stackoverflow.com/questions/19991445/run-an-ols-regression-with-pandas-data-frame
#        3. http://www.statsmodels.org/dev/examples/notebooks/generated/ols.html
#        4. https://pandas.pydata.org/pandas-docs/stable/dsintro.html
#        5. https://en.wikipedia.org/wiki/Multicollinearity
#   If the output "Cond. No."(Condition Number) is larger than 30, it indicates there are multicollinearity.
#       ref. 3 and 5.
#
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''Input File format example:'''
    print('''
    #input example, the fist line was treated as Dependent variable, following as indepen
    ------------------------
Y 1  2  3  4  3  4  5  4  5  5  4  5  4  5  4  5  6  5  4  5  4  3  4
T 4  2  3  4  5  4  5  6  7  4  8  9  8  8  6  6  5  5  5  5  5  5  5
M 4  1  2  3  4  5  6  7  5  8  7  8  7  8  7  8  7  7  7  7  7  6  5
K 4  1  2  5  6  7  8  9  7  8  7  8  7  7  7  7  7  7  6  6  4  4  4

    #output example
    ------------------------
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    titleColumn  = False
    zNormalized = False
    if args['-t']:
        titleColumn = True
    if args['-n']:
        zNormalized = True

    import numpy as np
    import statsmodels.api as sm
    import pandas as pd
    from collections import OrderedDict
    from scipy import stats

    y = pd.Series()
    x = OrderedDict()
    tempIndex = 1
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if y.empty:
                name='Y'
                data = []
                if titleColumn:
                    name=ss[0]
                    data = [float(x) for x in ss[1:]]
                    # y = pd.Series([float(x) for x in ss[1:]],name=ss[0])
                else:
                    data = [float(x) for x in ss]
                    # y = pd.Series([float(x) for x in ss],name='Y')
                if zNormalized:
                    data = stats.zscore(data)

                y = pd.Series(data, name=name)

            else:
                name=''
                data = []
                if titleColumn:
                    name = ss[0]
                    data = [float(x) for x in ss[1:]]
                    # x[ss[0]] = [float(x) for x in ss[1:]]
                else:
                    tempIndex += 1
                    name = 'x' + str(tempIndex)
                    data = [float(x) for x in ss]
                    # x['x' + str(tempIndex)] = [float(x) for x in ss]
                if zNormalized:
                    data = stats.zscore(data)

                x[name] = data

    x = pd.DataFrame(x)

    x = sm.add_constant(x)
    # print(x)
    # print(y)
    ols_model = sm.OLS(y, x)
    ols_results = ols_model.fit()
    print(ols_results.summary())

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
