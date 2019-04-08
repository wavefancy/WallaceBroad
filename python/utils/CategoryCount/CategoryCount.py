#!/usr/bin/env python3

"""
    -------------------------------------
    CategoryCount
    -------------------------------------

    @Author: wavefancy@gmail.com
    @Version: 2.0

    @Notes:
        1. Read category item(line by line) from stdin and output results to stdout.

    Get summary statistics from category data.
    @Author: wavefancy@gmail.com

    Usage:
        CategoryCount.py [-t name] [-s]
        CategoryCount.py -h | --help | -v | --version | -f | --format

    Options:
        -t name        Title name, default: GROUPNAME.
        -s             Output total summary.
        -h --help      Show this screen.
        -v --version   Show version.
        -f --format    Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def ShowFormat():
    '''Input File format example:'''
    print('''
# input:
------------------
1
2
1
3
3

# output:
# cat test.txt | python3 CategoryCount.py -s -t MYNAME
------------------
MYNAME  COUNT   FRACTION
1       2       0.400000
2       1       0.200000
3       2       0.400000
Total   5       1.0
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.1')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    NAME = args['-t'] if args['-t'] else 'GROUPNAME'
    OUT_SUMMARY = True if args['-s'] else False

    sys.stdout.write('%s\tCOUNT\tFRACTION\n'%(NAME))
    countMap = {}
    total = 0
    for line in sys.stdin:
        line = line.strip()
        if line:
            total = total +1
            if line in countMap:
                countMap[line] = countMap[line] + 1
            else:
                countMap[line] = 1

    # sort key and output results.
    for key in sorted(countMap.keys()):
        sys.stdout.write('%s\t%d\t%f\n'%(key, countMap[key], countMap[key] *1.0/total))

    if OUT_SUMMARY:
        sys.stderr.write('Total\t%d\t1.0\n'%(total))

    sys.stdout.flush()
    sys.stdout.close()
    sys.stderr.flush()
    sys.stderr.close()
