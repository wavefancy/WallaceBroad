#!/usr/bin/env python

"""

    Meta analysis by metap package in R, sumz method.
    # https://www.rdocumentation.org/packages/metap/versions/1.1/topics/sumz

    @Author: wavefancy@gmail.com

    Usage:
        MetaWeightedP.py
        MetaWeightedP.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin.
            Each line: groupName weight1 p1 weight2 p2 ...
        2. Output to stdout.
        3. Support signed P value. The sign will be assigned to weights beta meta.

    Options:
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
import numpy as np

def ShowFormat():
    '''Input File format example:'''
    print('''
#input example
#------------------------
G1 1 0.1 1 0.1
G2 1 0.1 1 -0.1
G3 1 0.2

#output example
#------------------------
GROUPNAME       MetaP   OLD_Ps
G1      3.4963e-02      1.0000e-01,1.0000e-01
G2      5.0000e-01      1.0000e-01,1.0000e-01
G3      2.0000e-01      2.0000e-01
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    # Call R function wilcox.test()
    from rpy2.robjects import FloatVector
    from rpy2.robjects.packages import importr
    metap = importr('metap')
    #http://rpy.sourceforge.net/rpy2/doc-dev/html/introduction.html
    def callMetaPSUMZ(p,singed_weights):
        '''Call R function sumz for the meta analysis'''
        # https://www.rdocumentation.org/packages/metap/versions/1.1/topics/sumz
        # print(p)
        # print(singed_weights)
        k = metap.sumz(FloatVector(p), weights= FloatVector(singed_weights))

        #z, p
        r = k[1][0]
        # print(r)
        return r

    sys.stdout.write('GROUPNAME\tMetaP\tOLD_Ps\n')
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                weights    = np.array([float(x) for x in ss[1::2]])
                p          = np.array([float(x) for x in ss[2::2]])

                # convert to singed weights, and unsigned P.
                weights[p<0] *= -1.0
                p[p<0] *= -1.0
                if len(p) == 1:
                    out = [ '%.4e'%(x) for x in [p[0], p[0]] ]
                else:
                    out = [ '%.4e'%(x) for x in [callMetaPSUMZ(list(p), list(weights))] + list(p) ]
                sys.stdout.write('%s\t%s\t%s\n'%(ss[0],out[0],','.join(out[1:])))

            except ValueError:
                sys.stderr.write('WARNING: parse value error, skip one line: %s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
