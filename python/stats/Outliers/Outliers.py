#!/usr/bin/env python

'''
    Outliers

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Algorithms:

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def help():
    sys.stderr.write('''
    -------------------------------------
    Outliers
    -------------------------------------

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Usages:
    para1: [int] Column index for values.
    para2: [int] the fold for SD. i.e.: 3|6

    @Notes:
    1. Detect outliers as MEAN (+/-) x*SD.
    2. Read from stdin and output to stdout.
    3. Column index starts from 1.
    -------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)

class P(object):
    col = -1
    fold = -1

if __name__ == '__main__':
    if len(sys.argv) != 3:
        help()

    P.col = int(sys.argv[1]) -1
    P.fold = int(sys.argv[2])

    content = [] # [(value, line), (value, line),()....]
    values = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split(None, P.col +1)
            try:
                vv = float(ss[P.col])
                values.append(vv)
                content.append((vv, line))
            except ValueError:
                sys.stderr.write('Warnning: can not parse value from this line: "%s"\n'%(line))

    import numpy as np
    std = np.std(values)
    mean = np.mean(values)
    left = mean - P.fold * std
    right = mean + P.fold * std

    sys.stderr.write('Mean\tSTD\tLx*STD\tRx*STD\n')
    sys.stderr.write('%.4f\t%.4f\t%.4f\t%.4f\n'%(mean, std, left, right))

    for v,l in content:
        if v < left or v > right:
            sys.stdout.write('%s\n'%(l))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
