#!/usr/bin/env python3

"""
    Keep/Remove records in range.

    @Author: wavefancy@gmail.com

    Usage:
        CheckInRange.py -r file -c int [-e]
        CheckInRange.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output result to stdout.
        2. Column index start from 1.

    Options:
        -c int        Column index for value.
        -r file       Range file, two columns, range_start range_end.
        -e            Exclude(Remove) records in defined range, default Include(Keep).
        -f --format   Show example.
        -h --help     Show this screen.
        -v --version  Show version.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def ShowFormat():
    print('''
# input
#-----------------
100     10
1000000 20
5000000 20
7000000 3
10000000 30

#range file:
#-----------------
1000000 5000000

# cat in.txt | python3 CheckInRange.py -r range.txt -c 1
#-----------------
1000000 20
5000000 20

cat in.txt | python3 CheckInRange.py -r range.txt -c 1 -e
#-----------------
100     10
7000000 3
10000000 30
    ''')

if __name__ == '__main__':
    args = docopt(__doc__, version='3.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)
#

    colValue  = int(args['-c']) -1
    keep = True
    if args['-e']:
        keep = False

    from interval import interval
    irange = interval()
    with open(args['-r'],'r') as inf:
        for line in inf:
            line = line.strip()
            if line:
                ss = line.split()
                irange = irange | interval[float(ss[0]), float(ss[1])]

#-------------------------------------------------
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                v = int(ss[colValue])
                if keep:
                    if v in irange:
                        sys.stdout.write('%s\n'%(line))
                else:
                    if not (v in irange):
                        sys.stdout.write('%s\n'%(line))

            except ValueError:
                sys.stderr.write('WARN: parse value error(skiped): %s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
