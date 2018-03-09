#!/usr/bin/env python3

"""

    Calculate AUC for label prediction.

    @Author: wavefancy@gmail.com

    Usage:
        auc.py
        auc.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and results to stdout.
        2. Each line two columns: label(binary,int), prediction_value.
        3. max(label) was considered positive label.

    Options:
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
# input example:
--------------------------
1       0.1
1       0.4
2       0.35
2       0.8

# output example:
--------------------------
7.5000e-01
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    import numpy as np
    from sklearn import metrics

    label=[]
    prediction = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                x = int(ss[0])
                y = float(ss[1])

                label.append(x)
                prediction.append(y)
            except ValueError:
                sys.stderr.write("WARN(skipped): parse value error at: %s\n"%(line))

    #Calculate AUC.
    fpr, tpr, thresholds = metrics.roc_curve(label, prediction, pos_label=max(label))
    sys.stdout.write('%.4f\n'%(metrics.auc(fpr, tpr)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
