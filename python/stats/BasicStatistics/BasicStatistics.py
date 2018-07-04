#!/usr/bin/env python3

'''
    Compute basic statistics

    @Author: wavefancy@gmail.com
    @Version: 1.0

'''

import sys
import numpy as np

def help():
    sys.stderr.write('''
    ---------------------------------------------
    Compute basic statistics for a column of data
    ---------------------------------------------

    @Autor: wavefancy@gmail.com
    @Version: 1.0

    @Usages:
    para1: column index for values,column starts from 1.
    ---------------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)

class P(object):
    col_index = 0  #column index for values.

def runApp():
    #read values from stdin
    vals = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                vals.append(float(ss[P.col_index]))
            except Exception as e:
                sys.stderr.write('WARN: parse value error, skipped: %s\n'%(line))

    sys.stdout.write('Min\t1%Q\tMean\tMedian\t99%Q\tMax\tSD\n')

    minV = min(vals)
    q1 = np.percentile(vals,1)
    meanV = np.mean(vals)
    medianV = np.median(vals)
    q99 = np.percentile(vals,99)
    #print(q99)
    maxV = max(vals)
    sdV = np.std(vals)

    #sys.stdout.write('%.4f\n'%(minV))
    sys.stdout.write('%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\n'%(minV,q1,meanV,medianV,q99, maxV, sdV))

    sys.stdout.close()

if __name__ == '__main__':

    if(len(sys.argv) != 2):
        help()

    P.col_index = int(sys.argv[1]) -1

    runApp()
