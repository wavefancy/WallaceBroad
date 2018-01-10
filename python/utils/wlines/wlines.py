#!/usr/bin/env python3

"""

    Copy lines to stdout.

    @Author: wavefancy@gmail.com

    Usage:
        wlines.py (-n index | -f file) [-e index] [-a number] [-r number]
        wlines.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output selected lines to stdout.
        2. Line index start from 1.

    Options:
        -n index      Set start line index, or Only copy this line to stdout if only this parameter in set.
        -e index      Set end line index, (inclusive).
        -a number     Set the end line as '-n index' + 'number', (inclusive).
        -r number     From start line, repeatly copy one line then skip 'number' lines, until reach file end.
        -f file       Read line index from 'file', one line one index, load all in memory.
        -h --help     Show this screen.
        -v --version  Show version.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

class P(object):
    start = -1 # start line index
    end = -1 # end line index
    nskip = -1
    lineSet = set()
    maxLine = -1 #maximum line index need to be output.

if __name__ == '__main__':
    args = docopt(__doc__, version='3.0')
    #print(args)
#
#     if(args['--format']):
#         ShowFormat()
#         sys.exit(-1)
# #

    if args['-n']:
        P.start = int(args['-n'])
    if args['-e']:
        P.end = int(args['-e'])
    if args['-a']:
        P.end = P.start + int(args['-a'])
    if args['-r']:
        P.nskip = int(args['-r'])
    if args['-f']:
        ll = [int(x) for x in open(args['-f'], 'r')]
        P.maxLine = max(ll)
        P.lineSet = set(ll)

#-------------------------------------------------
    temp = 0
    sCount = -1
    for line in sys.stdin:
        temp += 1
        if P.nskip < 0:             #no in repeat mode.
            if P.end <= 0:
                if P.lineSet:
                    if temp in P.lineSet:
                        sys.stdout.write(line)
                    if temp >= P.maxLine:
                        break

                elif temp == P.start:       #single line mode.
                    sys.stdout.write(line)
                    break
            else:
                if temp > P.end:
                 break;

                if temp >= P.start:
                    sys.stdout.write(line)
        else:                       #in repeat model.
            if temp >= P.start:
                sCount += 1
                if sCount == 0:
                    sys.stdout.write(line)
                if sCount == P.nskip:
                    sCount = -1

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
