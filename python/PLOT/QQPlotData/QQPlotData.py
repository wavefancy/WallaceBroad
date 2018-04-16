#!/usr/bin/env python3

"""

    Generate data for QQ plot.

    @Author: wavefancy@gmail.com

    Usage:
        QQPlotData.py -x xindex [-y yindex] [-k]
        QQPlotData.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output results (x,y) to stdout.
            (x,y) is the point for QQ plot.
        2. If input only have one dataset (-x), the other dataset(-y) will
            be generated from uniform distribution.

    Options:
        -x xindex     Column index for input data set one, index starts from 1.
        -y yindex     Column index for input data set two.
        -k            Keep the input content, add one column for expected value.
                        '-y' has to be switched off.
        -h --help     Show this screen.
        -v --version  Show version.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
#input
-------------------------------------------
A       0.1     0.2
B       0.8     0.9
C       0.3     0.5
D       0.7     0.4

#  cat test.txt | python3 QQPlotData.py -x 2 -k
-------------------------------------------
A       0.1     0.2     2.5720e-02
C       0.3     0.5     7.5769e-02
D       0.7     0.4     9.5750e-02
B       0.8     0.9     9.1152e-01

cat test.txt | python3 QQPlotData.py -x 2 -y 3
-------------------------------------------
1.0000e-01      2.0000e-01
3.0000e-01      4.0000e-01
7.0000e-01      5.0000e-01
8.0000e-01      9.0000e-01
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    xindex = int(args['-x']) -1
    yindex = -1
    if args['-y']:
        yindex = int(args['-y']) -1
    keepContent = False
    if args['-k']:
        if yindex >= 0:
            sys.stderr.write('ERROR: if set -k, please do not set -y.\n')
            sys.exit(-1)
        else:
            keepContent = True

    # xdata = []
    ydata = []
    content_with_x = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                x = float(ss[xindex])
                if yindex >= 0:
                    y = float(ss[yindex])
                    ydata.append(y)
                # xdata.append(x)
                content_with_x.append(ss + [x])

            except ValueError:
                sys.stderr.write('Parse value error (SKIPPED): %s\n'%(line))
    if not ydata:
        import random
        ydata = [random.random() for x in range(len(content_with_x))]

    #sort data and output.
    if keepContent:
        content_with_x = sorted(content_with_x, key=lambda x:x[-1])
        ydata = sorted(ydata)
        for x,y in zip(content_with_x,ydata):
            out = x[:-1]
            out.append('%.4e'%(y))
            sys.stdout.write('%s\n'%('\t'.join(out)))

    else:
        xdata = [x[-1] for x in content_with_x]
        for x,y in zip(sorted(xdata), sorted(ydata)):
            sys.stdout.write('%.4e\t%.4e\n'%(x,y))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
