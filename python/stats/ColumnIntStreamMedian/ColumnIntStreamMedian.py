#!/usr/bin/env python3

"""

    Compute the median for each column of int values.
    * Force the input values as int if not.
    * This program has been optimized to save memory for compute int median.

    @Author: wavefancy@gmail.com

    Usage:
        ColumnIntStreamMedian.py
        ColumnIntStreamMedian.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data with header from stdin.
        2. Default code the missing data 'nan'.
        3. Output results to stdout.
        4. Fource the input as int if not to save memory for search median.

    Options:
        -h --help       Show this screen.
        -v --version    Show version.
        -f --format     Show format example.
"""
import sys
from docopt import docopt
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
#----------------
A       B       C
1       10      3
0       1       3
1       2       4
-1      3       7
#----------------
STATS   A       B       C
MEDIAN  0.5     2.5     3.5
''')

# https://realpython.com/python3-object-oriented-programming/
import math
class IntMedian:
    def __init__(self):
        self.COUNT_MAP = {}
        self.TOTAL = 0
    
    def addOne(self, v):
        if np.isnan(v) == True:
            return
        else:
            v = int(v)
            if v not in self.COUNT_MAP:
                self.COUNT_MAP[v] = 0
            self.COUNT_MAP[v] += 1
            self.TOTAL += 1
    
    def getMedian(self):
        middle = math.ceil((self.TOTAL+0.1)/2)  # find the end positon for the middle point.
        temp = 0
        sorted_keys = sorted(self.COUNT_MAP.keys())
        point = 0
        for i in range(len(sorted_keys)):
            temp += self.COUNT_MAP[sorted_keys[i]]
            if temp >= middle:
                point = i
                break
        # temp_[point-1] < middle.
        if self.TOTAL%2 == 1 : # only need find a single number. total in odds.
            return sorted_keys[point]
        else: # we need two values for the average. total in even.
            if temp - self.COUNT_MAP[sorted_keys[point]] == middle-1:
                return (sorted_keys[point]+sorted_keys[point-1])/2.0
            else:
                return sorted_keys[point]

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)
    
    MISS = 'nan'
    SEP  = '\t'

    IntMedians  = [] # The object list to find int median.
    TITLE = False
    for line in sys.stdin:
        if not TITLE:
            sys.stdout.write('STATS\t'+line)
            l = len(line.strip().split())
            IntMedians = [IntMedian() for x in range(l)]
            TITLE = True
        else:
            ins = np.fromstring(line,sep=SEP)
            for o,i in zip(IntMedians, ins):
                o.addOne(i)
            
    out = [o.getMedian() for o in IntMedians]
    sys.stdout.write('MEDIAN\t%s\n'%('\t'.join(['%g'%(x) for x in out])))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
