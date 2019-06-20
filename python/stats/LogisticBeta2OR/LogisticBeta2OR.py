#!/usr/bin/env python3

"""

    Convert from logistic regression beta and se to OR, OR_SE, OR_CI
    Currently the default CI is 95%.

    @Author: wavefancy@gmail.com

    Usage:
        LogisticBeta2OR.py -b int -s int
        LogisticBeta2OR.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
            add three more columns for the values of OR, OR_SE and OR_95CI
        2. See example by -f.

    Options:
        -b int         Column index for the beta, index starts from 1.
        -s int         Column index for standard error of the beta.
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
Beta BetaSE
0.5 0.1
-0.3 0.2

#output
# cat test.txt | python3 LogisticBeta2OR.py -b 1 -s 2
#--------------
Beta BetaSE     OR      OR_SE   OR_CI_L OR_CI_R
0.5 0.1 1.6487  0.1649  1.3553  2.0057
-0.3 0.2        0.7408  0.1482  0.5006  1.0964
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

    beta = int(args['-b']) -1
    beta_se = int(args['-s']) -1

    TITLE_ADD = 'OR\tOR_SE\tOR_CI_L\tOR_CI_R'

    # CI: https://en.wikipedia.org/wiki/Standard_error
    # OR: https://www.stata.com/support/faqs/statistics/delta-rule/
    # ORb = exp(b)
    # se(ORb) = exp(b)*se(b)
    # Upper 95% limit: exp(b + 1.96 b_SE)
    # Lower 95% limit: exp(b - 1.96 b_SE)

    import numpy
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                b  = float(ss[beta])
                se = float(ss[beta_se])

                OR = numpy.exp(b)
                OR_SE = OR * se

                CI = 1.96 * se
                CIL = numpy.exp(b-CI)
                CIR = numpy.exp(b+CI)

                out = [OR, OR_SE, CIL, CIR]
                out = ['%.4f'%(x) for x in out]
                sys.stdout.write('%s\t%s\n'%(line, '\t'.join(out)))
            except Exception as e:
                sys.stdout.write('%s\t%s\n'%(line, TITLE_ADD))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
