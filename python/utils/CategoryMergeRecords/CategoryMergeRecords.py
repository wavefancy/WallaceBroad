#!/usr/bin/env python

"""

    Merge records for each category.

    @Author: wavefancy@gmail.com

    Usage:
        CategoryMergeRecords.py -k ints [-l]
        CategoryMergeRecords.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin (file name line by line), and output results to stdout.
        2. *** Input should be category based sorted. Entryies for the same category
               should be in successive.

    Options:
        -k ints       Column index for category, 1 based. eg. 1|1,3.
        -l            List all the content of the merged entries.
        --version     Show version.
        -f --format   Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)
import os.path as path

def ShowFormat():
    '''Input File format example:'''
    print('''
#-----INPUT-----
1	x c
1	y c
2	1 t
2	1 m

# OUTPUT: -k 1
#---------------
1       x,y     c
2       1       t,m

# OUTPUT: -k 1 -l
#---------------
1       x,y     c,c
2       1,1     t,m
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    CATEGORYS     = [int(x)-1 for x in args['-k'].split(',')]
    CATEGORYS_set = set(CATEGORYS)
    listALL       = True if args['-l'] else False

    from collections import OrderedDict
    def processOne(entries):
        '''Process the content of one category'''

        out = []
        for i in range(len(entries[0][1])): # each element of an array.
            # iterate across the entries, and merge the values of each element.
            # if the same value colapse as one, of not the keep the both.
            if listALL:
                # Columns for category name, they are the same, just pick the fist one.
                if i in CATEGORYS_set:
                    out.append(entries[0][1][i])
                else:
                    out.append(','.join([k[1][i] for k in entries]))

            else:
                keys = OrderedDict((k[1][i],None) for k in entries).keys()
                out.append(','.join(keys))
        # print(out)
        sys.stdout.write('%s\n'%('\t'.join(out)))

    #read from stdin.
    c_temp = [] #[(entryName,entry1), (entryName,entry2)... ] #entries for a category.
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            name = ','.join([ss[x] for x in CATEGORYS])
            if c_temp:
                if c_temp[-1][0] == name:
                    c_temp.append((name,ss))
                else:
                    processOne(c_temp)
                    c_temp = []
                    c_temp.append((name,ss))
            else:
                c_temp.append((name,ss))

    #deal with the last category.
    processOne(c_temp)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
