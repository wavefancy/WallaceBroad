#!/usr/bin/env python

"""

    Select entries based on unique or duplicated key. 
    Like Unix `uniq`, but the uniqueness was determinded by key only.

    @Author: wavefancy@gmail.com

    Usage:
        CategoryUnique.py -k ints (-u | -d)
        CategoryUnique.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin (file name line by line), and output results to stdout.
        2. **** INPUT SHOULD BE SORTED BY CATEGORY NAMES ****
              Treat successive same -k column values as a single category.

    Options:
        -k ints     Column index for category, 1 based. eg. 1|1,3.
        -u          Output entries with unique key.
        -d          Output entries with duplicated key.
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
# INPUT:
2   ss  1
2   ss  2
3   ss  3
4   ss  3

# cat test.txt | python3 CategoryUnique.py -k 1 -d
2   ss  1
2   ss  2

cat test.txt | python3 CategoryUnique.py -k 1 -u
3   ss  3
4   ss  3
    ''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    CATEGORYS   = [int(x)-1 for x in args['-k'].split(',')]
    DUPLICATE   = True if args['-d'] else False

    def processOne(entries):
        '''Out put one category'''
        if DUPLICATE:
            if len(entries) > 1:
                for _,v in entries:
                    sys.stdout.write('%s\n'%(v))
        else:
            if len(entries) == 1:
                for _,v in entries:
                    sys.stdout.write('%s\n'%(v))

    #read from stdin.
    c_temp = [] #[(entryName,entry1), (entryName,entry2)... ] #entries for a category.
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            name = ','.join([ss[x] for x in CATEGORYS])
            if c_temp:
                if c_temp[-1][0] == name:
                    c_temp.append((name,line))
                else:
                    processOne(c_temp)
                    c_temp = []
                    c_temp.append((name,line))
            else:
                c_temp.append((name,line))

    #deal with the last category.
    processOne(c_temp)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
