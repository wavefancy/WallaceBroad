#!/usr/bin/env python

"""

    Bootstrapping the difference of two numbers.
    - Random pick up two from samples(without replacement) and compute the difference.
    - Bootstrapping the process N times.

    @Author: wavefancy@gmail.com

    Usage:
        BootDifferenceOf2.py -n int
        BootDifferenceOf2.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout. Input one column with values.
        2. Output results from stdout.

    Options:
        -n int        Number of bootstrappings.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
#   Ref:
#        1. https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
#
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''Input File format example:'''
    print('''
#input example
------------------------
1
2
3
4
5
6
7
8

# -n 3
------------------------
4.0000e+00
-3.0000e+00
-2.0000e+00
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    BTIMES = int(args['-n'])
    data = []
    [data.append(float(x)) for x in sys.stdin]

    import random
    for _ in range(BTIMES):
        xy = random.sample(data,2)
        diff = xy[0] - xy[1]
        sys.stdout.write('%.4e\n'%(diff))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
