#!/usr/bin/env python

"""

    Meta analysis of Chisq statistics. 
        The sum of X2 is still X2 with the sum of degree of freedom.
    https://online.stat.psu.edu/stat414/node/171/

    @Author: wavefancy@gmail.com

    Usage:
        MetaX2.py
        MetaX2.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin.
            Each line: groupName Degree_1 X2_1 Degree_2 X2_2 ...
        2. Output to stdout.
        3. The missing value was coded as 'NA'.

    Options:
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
import numpy as np
from scipy.stats import chi2

def ShowFormat():
    '''Input File format example:'''
    print('''
#input example
#------------------------
X 1 2.2 3 1.1
Y 1 3 3 3
T NA 2 2 3

#output example
#------------------------
GROUPNAME       DOF     X2      PVAL
X       4       3.3     0.508932
Y       4       6       0.199148
    ''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    sys.stdout.write('GROUPNAME\tDOF\tX2\tPVAL\n')
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            
            DOF = np.array([x for x in ss[1::2]])
            X2S = np.array([x for x in ss[2::2]])

            data_i = np.logical_and(DOF !=  'NA', DOF != 'NA')

            try:
                total_dof = DOF[data_i].astype(np.int).sum()
                total_x2  = X2S[data_i].astype(np.float).sum()
                
                if total_dof > 0:
                    pv = chi2(total_dof).sf(total_x2)
                    sys.stdout.write('%s\t%s\n'%(ss[0],'\t'.join(['%g'%(x) for x in (total_dof, total_x2, pv)])))
                else:
                    sys.stdout.write('%s\tNA\tNA\tNA\n'%(ss[0]))
            except:
                sys.stderr.write('WARN: value parse error at: %s\n'%(line))
            
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
