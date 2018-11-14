#!/usr/bin/env python3

"""

    Calculate pvalue for Mann-Whitney U test. Call wilcox.test function from R by rpy2.
    @Author: wavefancy@gmail.com

    Usage:
        mannWhitneyUtestR.py [-a int] [-l]
        mannWhitneyUtestR.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout.
        2. Compute exact pvalue for small number of input.
        3. Output **One-sided p-value**.
        4. Detail R wilcox.test.

    Options:
        -a int        -1|0|1, Alternative test, default 0 for test two.sided.
                      -1 for less, 1 for greater.
        -l            Indicate the first column in each data set as label, output label also.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''Input File format example:'''
    print('''
#input example, each line two samples, separated by ';'
------------------------
0.80 0.83 1.89 1.04 1.45 1.38 1.91 1.64 0.73 1.46; 1.15 0.88 0.90 0.74 1.21

#output example (benchmarked with R, wilcox.test)
------------------------
0.2544122544122544

# first column as label: -l
------------------------
X 0.80 0.83 1.89 1.04 1.45 1.38 1.91 1.64 0.73 1.46; Y 1.15 0.88 0.90 0.74 1.21

#output example (benchmarked with R, wilcox.test)
------------------------
X       Y       0.2544122544122544

    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    Alternative = 'two.sided'
    if args['-a'] == '-1':
        Alternative = 'less'
    elif args['-a'] == '1':
        Alternative = 'greater'
    WITH_LABEL = True if args['-l'] else False

    # Call R function wilcox.test()
    from rpy2.robjects import FloatVector
    from rpy2.robjects.packages import importr
    stats = importr('stats')
    #http://rpy.sourceforge.net/rpy2/doc-dev/html/introduction.html
    def callRWilcoxTest(x,y):
        '''Call R function to do wilcox.test'''
        k = stats.wilcox_test(FloatVector(x),FloatVector(y),alternative=Alternative)
        return list(k[2])[0] # for pvalue.

    # data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = [x.strip() for x in line.split(';')]
            try:
                # print(ss)
                left  = ss[0].split()
                right = ss[1].split()
                if WITH_LABEL:
                    x = [float(x) for x in left[1:] if x]
                    y = [float(x) for x in right[1:] if x]
                    sys.stdout.write('%s\t%s\t%s\n'%(left[0],right[0],callRWilcoxTest(x,y)))

                else:
                    x = [float(x) for x in left if x]
                    y = [float(x) for x in right if x]
                    sys.stdout.write('%s\n'%(callRWilcoxTest(x,y)))

            except ValueError:
                sys.stderr.write('WARNING: parse value error, skip one line: %s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
