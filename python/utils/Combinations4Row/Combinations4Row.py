#!/usr/bin/env python3

'''

    Output all the possible combinations for row.

    @Author: wavefancy@gmail.com, Wallace Wang.

    Usage:
        Combinations4Row.py [-n int]
        Combinations4Row.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.

    Options:
        -n int        Set the number of element picking up each time, default len(input_data).
        -h --help     Show this screen.
        --version     Show version.
        -f --format   Show input/output file format example.

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.
from docopt import docopt

def ShowFormat():
    '''File format example'''
    print('''
#Input file format(stdin)
------------------------
1
2
3

#cat test.txt | python3 Combinations4Row.py -n 2
------------------------
1;2
1;3
2;3
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    PICK_NUM      = int(args['-n']) if args['-n'] else None
    OUT_DELIMITER = ';'
    from itertools import combinations

    data = []
    for line in sys.stdin:
        line = line.strip()
        if line :
            data.append(line)

    # read data in.
    if not PICK_NUM:
        PICK_NUM = len(data)
    # print(data)
    for out in combinations(data,PICK_NUM):
        # print(out)
        sys.stdout.write('%s\n'%(OUT_DELIMITER.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
