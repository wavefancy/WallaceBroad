#!/usr/bin/env python3

"""

    Estimate the binomial P (the probability of true) for each category.
    # Estimation detail:
    # http://moonvalley.guhsdaz.org/common/pages/DisplayFile.aspx?itemId=17682112

    @Author: wavefancy@gmail.com

    Usage:
        CategoryBinomialP.py
        CategoryBinomialP.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and results to stdout.
        2. Each line two columns: category name, 0/1.
        3. Output as three column: name P Standard_Deviation_of_P

    Options:
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from collections import OrderedDict
from math import sqrt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
# input example:
--------------------------
A 1
A 1
A 0
B 1
B 0

# output example:
--------------------------
GROUP   P       P_SD
A       0.666667        0.272166
B       0.5     0.353553
    ''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    VALID_VALUE_SET = set(['0','1'])


    data = OrderedDict() # name -> [count_of_0, count_of_1]
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[1] not in VALID_VALUE_SET:           
                sys.stderr.write("WARN(skipped): the value is not 0/1: %s\n"%(line))
            else:
                if ss[0] not in data:
                    data[ss[0]] = [0,0]
                
                if ss[1] == '0':
                    data[ss[0]][0] += 1
                else:
                    data[ss[0]][1] += 1

    sys.stdout.write('GROUP\tP\tP_SD\n')
    for k in data.keys():
        N = sum(data[k])
        P  = data[k][1]/N
        sd = sqrt(P*(1-P)*1.0/N)
        out = [k, '%g'%(P), '%g'%(sd)]

        sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
