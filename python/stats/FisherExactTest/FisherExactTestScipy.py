#!/usr/bin/env python3

"""

    FisherExactTest for 2by2 table.
    @Author: wavefancy@gmail.com

    Usage:
        FisherExactTestScipy.py -c cols -t cols [-a alternative] [--pd int]
        FisherExactTestScipy.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout,
            *** add two columns for pvalue and odds ratio
            *** If there are 0 in some cells, add each cell by 0.5 for estimate odds ratio.
        2. See example by -f.

    Options:
        -c cols        Column indexes for treat1, eg: 1,2. Index started from 1.
        -t cols        Column indexes for treat2, eg: 3,4. Index started from 1.
        -a int         [1|2] Alternative for the test, default 0:'two-sided',
                       1: 'less',     test depletion  of the first element in treat1.
                       2: 'greater',  test enrichment of the first element in treat1.
        --pd int       Print int decimal points.
        -h --help      Show this screen.
        -v --version   Show version.
        -f --format    Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
from scipy import stats
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
    alternative = 'two-sided'
    if args['-a']:
        if args['-a'] == '1':
            alternative = 'less'
        elif args['-a'] == '2':
            alternative = 'greater'
    pdecimal = int(args['--pd']) if args['--pd'] else 4

    t1Index = [int(x) -1 for x in args['-c'].split(',')]
    t2Index = [int(x) -1 for x in args['-t'].split(',')]


    INF = float('inf')
    fstring = '%.'+str(pdecimal)+'f'
    estring = '%.'+str(pdecimal)+'e'
    # print(fstring)
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                c1 = [int(ss[x]) for x in t1Index]
                c2 = [int(ss[x]) for x in t2Index]

                oddsratio, pvalue = stats.fisher_exact([c1, c2])

                # if out[1] == 0 or out[1] == INF:
                #     oddsratio = (c1[0]+0.5) / (c1[1] + 0.5) / ((c2[0] + 0.5) / (c2[1] + 0.5))
                #     out[1] = oddsratio

                sys.stdout.write('%s\t'%(line))
                sys.stdout.write('%s\t'%(estring%(pvalue)))
                sys.stdout.write('%s'%(estring%(oddsratio)))
                # sys.stdout.write('\t'.join([fstring%(x) for x in out[1:]]))
                sys.stdout.write('\n')
            except ValueError:
                # sys.stderr.write('WARNING: parse int error for line(skipped): %s\n'%(line))
                sys.stderr.write('%s\tNA\tNA\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
