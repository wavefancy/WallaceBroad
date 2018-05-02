#!/usr/bin/env python3

"""

    Split comma separated records.

    Usage:
        SplitRecord.py -a columnIndexs
        SplitRecord.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output results to stdout.
        3. See example by -f.

    Options:
        -a columnIndexs  Column index for split, eg: 1,2,3|2
        -h --help        Show this screen.
        -v --version     Show version.
        -f --format      Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
# intput: -a 4,5
#------------------------------------
1       13370   T       C       1.55039e-04
1       13372   G       T,C     1.56446e-04,8.18833e-04
1       13379   A       C       3.23520e-04

# output
#------------------------------------
1       13370   T       C       1.55039e-04
1       13372   G       T       1.56446e-04
1       13372   G       C       8.18833e-04
1       13379   A       C       3.23520e-04
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    cols = set([int(x)-1 for x in args['-a'].split(',')])

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()

            temp = []
            t_len = 1
            for i in range(len(ss)):
                if i in cols:
                    t = ss[i].split(',')
                    t_len = len(t)
                else:
                    t = ss[i]
                temp.append(t)

            #output results:
            for j in range(t_len):
                out = []
                for i in range(len(ss)):
                    if i in cols:
                        out.append(temp[i][j])
                    else:
                        out.append(temp[i])

                sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
