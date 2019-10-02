#!/usr/bin/env python

"""

    Select the extreme value for each category.

    @Author: wavefancy@gmail.com

    Usage:
        CategoryExtreme.py -k ints -v int [-o txt | --txt] (--max | --min) [-a]
        CategoryExtreme.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin (file name line by line), and output results to stdout.
        2. **** INPUT SHOULD BE SORTED BY CATEGORY NAMES ****
              Treat successive same -k column values as a single category.

    Options:
        -k ints     Column index for category, 1 based. eg. 1|1,3.
        -v int      Column index for value, 1 based. eg. 1.
        -o txt      Order for ranking category data, small to large. eg. ONE,TWO,THREE.
        -a          Select all entries with extreme value, default random pick one.
        --txt       Sort by value text string naturally, do not convert to float.
        --max       Select the maxmium values for each category.
        --min       Select the minimum values for each category.
        --version  Show version.
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

    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    CATEGORYS   = [int(x)-1 for x in args['-k'].split(',')]
    VALUE       = int(args['-v'])-1
    MAX_VAL     = True if args['--max'] else False
    ALL_EXTREME = True if args['-a'] else False
    ORDERS      = args['-o'].split(',') if args['-o'] else []
    ORDERS_MAP  = {k:i for (i,k) in enumerate(ORDERS)}
    TEXT_SORT   = True if args['--txt'] else False

    def processOne(entries):
        '''find out the extreme value and output'''
        ee = ''
        vv = []
        if TEXT_SORT:
            if MAX_VAL:
                entries.sort(key=lambda x: x[1][VALUE], reverse=True)
            else:
                entries.sort(key=lambda x: x[1][VALUE])

        elif ORDERS:
            if MAX_VAL:
                entries.sort(key=lambda x: ORDERS_MAP[x[1][VALUE]], reverse=True)
            else:
                entries.sort(key=lambda x: ORDERS_MAP[x[1][VALUE]])

        else:
            if MAX_VAL:
                entries.sort(key=lambda x: float(x[1][VALUE]), reverse=True)
            else:
                entries.sort(key=lambda x: float(x[1][VALUE]))

        #output results after sort.
        if ALL_EXTREME:
            for _,v in entries:
                if v[VALUE] == entries[0][1][VALUE]:
                    sys.stdout.write('\t'.join(v))
                    sys.stdout.write('\n')
                else:
                    break
        else:
            sys.stdout.write('\t'.join(entries[0][1]))
            sys.stdout.write('\n')

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
