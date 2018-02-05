#!/usr/bin/env python3

"""

    Power estimation for T-Test.

    @Author: wavefancy@gmail.com

    Usage:
        PowerEstimationTTest.py [-g spliter] [-t spliter] [-i inputType]
        PowerEstimationTTest.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and results to stdout.
        2. Output sample size was ceiled to float x, smallest integer number needed.

    Options:
        -i inputType  Set input format type. Default 1.
        -g spliter    Set spliter for group, default ';'.
        -t spliter    Set group title spliter, default ':'.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
# input example: -i 1
--------------------------
t1: 1 2 3 4;t2: 6 7 8 9 11
1 2 3 4;6 7 8 9 11
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    gspliter = ';'
    tspliter = ':'
    iType = '1'

    if args['-g']:
        gspliter = args['-g']
    if args['-t']:
        gspliter = args['-t']
    if args['-i']:
        iType = args['-i']

    import statsmodels.stats.power as smp
    import math
    power = 0.8
    alpha = 0.05
    alternative = 'two-sided'
    ratio = 1

    def estimatePowerN(m1, m2, var1, var2, n1, n2):
        '''Estimate sample size needed.
           m: mean
           var: variance
           v: sample size.
           Ref: webpower_manual_book, page 61.
        '''
        sp = pow((((n1-1)*var1 + (n2-1)*var2) / (n1 + n2 - 2)),0.5)
        # print(sp)
        # print(m1-m2)
        effectSize = (m1-m2)/sp
        # print(effectSize)
        re = smp.TTestIndPower().solve_power(abs(effectSize), power=power, ratio=ratio, alpha=alpha, alternative=alternative)
        # print(re)
        # ceil(x)
        #Return the ceiling of x as a float, the smallest integer value greater than or equal to x.
        # print(re)
        return math.ceil(re)

#-------------------------------------------------
    if iType == '1':
        import numpy as np

        for line in sys.stdin:
            line = line.strip()
            if line:
                gg = line.split(';')
                g1 = gg[0].split(':')
                g2 = gg[1].split(':')
                # print(gg)

                d1 = []
                d2 = []
                t1 = ''
                t2 = ''
                if len(g1) == 2:
                    d1 = [float(x) for x in g1[1].strip().split()]
                    t1 = g1[0].strip()
                else:
                    d1 = [float(x) for x in g1[0].strip().split()]

                if len(g2) == 2:
                    d2 = [float(x) for x in g2[1].strip().split()]
                    t2 = g2[0].strip()
                else:
                    d2 = [float(x) for x in g2[0].strip().split()]

                m1 = np.mean(d1)
                m2 = np.mean(d2)
                var1 = np.var(d1)
                var2 = np.var(d2)

                out = ''
                if t1 and t2:
                    out = t1 + '-' + t2 + '\t'
                out += '%d'%(estimatePowerN(m1, m2, var1, var2, len(d1), len(d2)))
                sys.stdout.write('%s\n'%(out))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
