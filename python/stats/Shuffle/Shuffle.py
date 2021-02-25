#!/usr/bin/env python3

"""
    Shuffle/Sample with/without replacement from the lines of stdin.

    @Author: wavefancy@gmail.com

    Usage:
        Shuffle.py [-n int] [-w] [-s txt] [-t]
        Shuffle.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output to stdout.

    Options:
        -n int        The number of records send to output after shuffle, default all lines.
        -w            Sample the records with replacement, default without replacement.
        -s txt        Specify the random seed, default `current system time`.
        -t            Set the first line as title, direct output.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.
"""
import sys
import random
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def ShowFormat():
    '''File format example'''
    print('''
#Input file format(stdin)
------------------------
A 1
B 2
C 3
D 4

cat test.txt | python Shuffle.py -n 3 -w -s 0
------------------------
B 2
D 4
B 2
''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    SEED            = args['-s']      if args['-s'] else None
    WITH_PLACEMENT  = True            if args['-w'] else False
    N_MAX           = int(args['-n']) if args['-n'] else -1
    WITH_TITLE      = True            if args['-t'] else False

    content = []
    for line in sys.stdin:
            if line:
                if WITH_TITLE:
                    # Output title
                    sys.stdout.write(line)
                    WITH_TITLE = False
                else:
                    content.append(line)

    if N_MAX < 0:
        N_MAX = len(content)

    # print(content)
    # print(N_MAX)
    random.seed(SEED)
    # https://docs.python.org/3/library/random.ht
    out = random.choices(content,k=N_MAX) if WITH_PLACEMENT else random.sample(content,k=N_MAX)

    for x in out:
        sys.stdout.write(x)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
