#!/usr/bin/env python3

"""

    Compute basic statistics for a each category.

    @Author: wavefancy@gmail.com

    Usage:
        BasicStatistics4Category.py [-t] [-m] [--mv string]
        BasicStatistics4Category.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.

    Options:
        -t            Output title.
        -m            Output the proportion of missing for each category.
        --mv string   Value for missing, default 'NA'.
        -l            Treat the first column as label, and output label for each row.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
#input:
------------------------
t       1   2   3
x       4   5   6
x       1   2   NA

#output: cat test.txt | python BasicStatistics4Category.py -m -t
------------------------
Category        %Missing
t       0.0000
x       0.1667

#output: cat in.txt | python3 BasicStatistics4Category.py -t
------------------------
Category        Min     1%Q     25%Q    Mean    Median  75%Q    99%Q    Max     SD      SE
t       1.0000  1.5000  1.5000  2.0000  2.0000  2.5000  2.9800  3.0000  0.8165  0.5774
x       1.0000  2.0000  2.0000  3.6000  4.0000  5.0000  5.9600  6.0000  1.8547  0.9274
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    oMissing = True if args['-m'] else False
    missing = args['--mv'] if args['--mv'] else 'NA'

    if args['-t']:
        if args['-m']:
            sys.stdout.write('Category\t%Missing\n')
        else:
            sys.stdout.write('Category\tMin\t1%Q\t25%Q\tMean\tMedian\t75%Q\t99%Q\tMax\tSD\tSE\n')

    from collections import OrderedDict
    dataMap = OrderedDict() #categoryname -> [float, float ... ]

    import numpy as np
    from scipy import stats
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0] not in dataMap:
                dataMap[ss[0]] = []
            dataMap[ss[0]] = dataMap[ss[0]] + ss[1:]

    #for the calculation.
    if oMissing:
        for k,v in dataMap.items():
            m = [x for x in v if x == missing]
            sys.stdout.write('%s\t%.4f\n'%(k, len(m)*1.0/len(v)))
    else:
        for k,v in dataMap.items():
            vals = [float(x) for x in v if x != missing]

            # vals = []
            # olabel = ''
            # if label:
            #     vals = [float(x) for x in ss[1:] if x != 'NA']
            #     olabel = ss[0]
            # else:
            #     vals = [float(x) for x in ss if x != 'NA']

            minV = min(vals)
            q1 = np.percentile(vals,1)
            q25 = q1 = np.percentile(vals,25)
            meanV = np.mean(vals)
            medianV = np.median(vals)
            q75 = np.percentile(vals,75)
            q99 = np.percentile(vals,99)
            #print(q99)
            maxV = max(vals)
            sdV = np.std(vals)
            se = stats.sem(vals)
            # if label:
            sys.stdout.write('%s\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\n'%(k,minV,q1,q25,meanV,medianV,q75,q99, maxV, sdV, se))
            # else:
                # sys.stdout.write('%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\n'%(minV,q1,q25,meanV,medianV,q75,q99, maxV, sdV, se))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
