#!/usr/bin/env python3

"""
    Keep/Remove records in range.

    @Author: wavefancy@gmail.com

    Usage:
        CheckInRangeCHR.py -r file -c int -p int [-e] [-t]
        CheckInRangeCHR.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output result to stdout.
        2. Column index start from 1.

    Options:
        -c int        Column index for chr.
        -p int        Column index for position(value to be checked in range).
        -r file       Range file, three columns, chr range_start range_end.
        -e            Exclude(Remove) records in defined range, default Include(Keep).
        -t            Treat the fist line as title.
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
chr1 100        10
chr1 1000000 20
chr2 5000000 20
chr2 7000000 3
chr2 10000000 30

#range file:
#-----------------
chr1 1000000 5000000

# cat in.chr.txt | python3 CheckInRangeCHR.py -r range.chr.txt -c 1 -p 2
#-----------------
chr1 1000000 20
    ''')

if __name__ == '__main__':
    args = docopt(__doc__, version='3.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)
#

    colValue  = int(args['-p']) -1
    colChr = int(args['-c']) -1
    keep = True
    if args['-e']:
        keep = False
    title = False
    if args['-t']:
        title = True

    # from interval import interval
    # https://pyinterval.readthedocs.io/en/latest/install.html#installing-from-sources
    # change to a a faster version of range search, use interlap.
    # https://github.com/brentp/interlap

    from interlap import InterLap
    from interlap import Interval # This class can auto merge overlapped regions.
    # interlap really significantly increased the search speed.

    itvMap = {} #chr - >intervals.
    #irange = interval()
    with open(args['-r'],'r') as inf:
        for line in inf:
            line = line.strip()
            if line:
                ss = line.split()
                if not (ss[0] in itvMap):
                    itvMap[ss[0]] = Interval()

                itvMap[ss[0]].add([(float(ss[1]), float(ss[2]))]) # auto merge region.

    checkMap = {}
    for k,v in itvMap.items():
        inter = InterLap()
        inter.update(v._as_tuples(v))
        checkMap[k] = inter # convert inverval to trees.
        # for i in inter:
        #     print(i)
#-------------------------------------------------
    # print(checkMap)
    for line in sys.stdin:
        line = line.strip()
        if line:
            if title:
                sys.stdout.write('%s\n'%(line))
                title = False
                continue

            ss = line.split()
            try:
                v = float(ss[colValue])
                if keep:
                    if ss[colChr] in checkMap and checkMap[ss[colChr]].__contains__((v,v)):
                        sys.stdout.write('%s\n'%(line))
                else:
                    if (ss[colChr] not in checkMap)  or ( not (checkMap[ss[colChr]].__contains__((v,v)))):
                        sys.stdout.write('%s\n'%(line))

            except ValueError:
                sys.stderr.write('WARN: parse value error(skiped): %s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
