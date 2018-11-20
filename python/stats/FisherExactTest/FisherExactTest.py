#!/usr/bin/env python3

"""

    FisherExactTest for 2by2 table.
    @Author: wavefancy@gmail.com

    Usage:
        FisherExactTest.py -c cols -t cols [-a alternative] [--ci float]
        FisherExactTest.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout,
            *** add four columns for pvalue and odds ratio, confidence_interval_left, confidence_interval_right.
            *** If there are 0 in some cells, add each cell by 0.5 for estimate odds ratio.
        2. See example by -f.

    Options:
        -c cols        Column indexes for treat1, eg: 1,2. Index started from 1.
        -t cols        Column indexes for treat2, eg: 3,4. Index started from 1.
        -a int         [1|2] Alternative for the test, default 0:'two-sided',
                       1: 'less',     test depletion  of the first element in treat1.
                       2: 'greater',  test enrichment of the first element in treat1.
        --ci float     Confidence interval, default 0.95.
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
#example input
-----------------------------
x1  7   0   186 95
x2  31  10  3183    1731
x3  x   x   x   x

# cat test.txt | python3 FisherExactTest.py -c 2,3 -t 4,5 --ci 0.9
-----------------------------
x1  7   0   186 95      9.9849e-02      7.6810e+00      9.0450e-01      inf
x2  31  10  3183    1731        1.8838e-01      1.6857e+00      8.9080e-01      3.1919e+00
x3  x   x   x   x       NA      NA      NA      NA
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    #api:
    #http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisher_exact.html
    # 'two-sided', 'less', 'greater'
    alternative = 'two.sided'
    if args['-a']:
        if args['-a'] == '1':
            alternative = 'less'
        elif args['-a'] == '2':
            alternative = 'greater'

    t1Index = [int(x) -1 for x in args['-c'].split(',')]
    t2Index = [int(x) -1 for x in args['-t'].split(',')]

    ci_alpha = float(args['--ci']) if args['--ci'] else 0.95

    from rpy2.robjects import FloatVector,IntVector
    from rpy2.robjects.packages import importr
    import rpy2
    exact = importr("exact2x2")

    INF = float('inf')
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                c1 = [int(ss[x]) for x in t1Index]
                c2 = [int(ss[x]) for x in t2Index]
                # print(IntVector(c1+c2))
                m = rpy2.robjects.r.matrix(IntVector(c1+c2),nrow=2,byrow="T")
                # print(ci_alpha)
                r = exact.exact2x2(m,tsmethod="minlike",alternative=alternative,conf_level=ci_alpha)

                out = []
                out.append(r[r.names.index('p.value')][0])
                out.append(r[r.names.index('estimate')][0])
                out.append(r[r.names.index('conf.int')][0])
                out.append(r[r.names.index('conf.int')][1])

                if out[1] == 0 or out[1] == INF:
                    oddsratio = (c1[0]+0.5) / (c1[1] + 0.5) / ((c2[0] + 0.5) / (c2[1] + 0.5))
                    out[1] = oddsratio

                sys.stdout.write('%s\t'%(line))
                sys.stdout.write('%.4e\t'%(out[0]))
                sys.stdout.write('\t'.join(['%.4f'%(x) for x in out[1:]]))
                sys.stdout.write('\n')
            except ValueError:
                # sys.stderr.write('WARNING: parse int error for line(skipped): %s\n'%(line))
                sys.stderr.write('%s\tNA\tNA\tNA\tNA\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
