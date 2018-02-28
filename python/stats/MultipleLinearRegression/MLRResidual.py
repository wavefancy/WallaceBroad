#!/usr/bin/env python

"""

    Perform multiple linear regression, Y ~ X1 + X2 + ... Xn,
    Add output the residual. Y - Y^hat, observed - predicted.
    @Author: wavefancy@gmail.com

    Usage:
        MLRResidual.py
        MLRResidual.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout.
        2. Output results from stdout.

    Options:
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
#        For residuals.
#        6. http://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.html
#        7. https://stackoverflow.com/questions/35417111/python-how-to-evaluate-the-residuals-in-statsmodels
#   If the output "Cond. No."(Condition Number) is larger than 30, it indicates there are multicollinearity.
#       ref. 3 and 5.
#
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''Input File format example:'''
    print('''
    #input example, the fist column was treated as Dependent variable, following as independent.
    ------------------------
Y       X1      X2
1       2       3
4       2       3
5       1       3
6       6       1
7       1       3

    #output example
    ------------------------
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    import numpy as np
    import statsmodels.api as sm
    import pandas as pd
    from collections import OrderedDict
    from scipy import stats

    #load data from stdin.
    x = pd.read_table(sys.stdin)
    y = x[x.columns[0]]
    x = x[x.columns[1:]]

    x = sm.add_constant(x)

    ols_model = sm.OLS(y, x)
    ols_results = ols_model.fit()
    sys.stderr.write('%s\n'%(str(ols_results.summary())))
    sys.stdout.write('%s\n'%('\n'.join(['%.4e'%(x) for x in ols_results.resid.tolist()])))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
