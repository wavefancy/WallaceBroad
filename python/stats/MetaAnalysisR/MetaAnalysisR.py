#!/usr/bin/env python

"""

    Meta analysis by R package metafor, rma method.
    # https://www.rdocumentation.org/packages/metafor/versions/1.9-9/topics/rma.uni

    @Author: wavefancy@gmail.com

    Usage:
        MetaAnalysisR.py [-m txt]
        MetaAnalysisR.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin.
            Each line: groupName beta1 beta1_se beta2 beta2_se ...
        2. Output to stdout.
        3. Detail R metafor.rma method.

    Options:
        -m txt        fixed- or a random/mixed-effects model, REML|FE.
                          FE: fixed-effects. REML: random effects(default).
                          More supported models please refer to R document.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''Input File format example:'''
    print('''
#input example
#------------------------
1:63063256-63070355_LOF+TG75    -0.41112        0.28037 -0.34896        0.31244 -1.7442 1.0482
1:63063256-63070355_LOF+5D-TG75 -0.45688        0.28432 -0.36746        0.32622 -1.6782 1.0524

#output example
#------------------------
GROUPNAME                       BETA            BETA_SE         ZVAL            PVAL            95CIL           95CIU
1:63063256-63070355_LOF+TG75    -4.3527e-01     2.0466e-01      -2.1268e+00     3.3434e-02      -8.3638e-01     -3.4150e-02
1:63063256-63070355_LOF+5D-TG75 -4.6846e-01     2.1003e-01      -2.2305e+00     2.5716e-02      -8.8010e-01     -5.6814e-02
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    MODEL = args['-m'] if args['-m'] else 'REML'

    # Call R function wilcox.test()
    from rpy2.robjects import FloatVector
    from rpy2.robjects.packages import importr
    metafor = importr('metafor')
    #http://rpy.sourceforge.net/rpy2/doc-dev/html/introduction.html
    def callRWilcoxTest(beta,beta_se):
        '''Call R function to do wilcox.test'''
        k = metafor.rma(yi=FloatVector(beta),sei=FloatVector(beta_se),method=MODEL)

        #beta, se, zval, pval, 95ci.l, 95ci.u
        r = (k[1][0],k[2][0],k[3][0],k[4][0],k[5][0],k[6][0])
        return r

    sys.stdout.write('GROUPNAME\tBETA\tBETA_SE\tZVAL\tPVAL\t95CIL\t95CIU\n')
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                beta    = [float(x) for x in ss[1::2]]
                beta_se = [float(x) for x in ss[2::2]]

                out = [ '%.4e'%(x) for x in callRWilcoxTest(beta,beta_se)]
                sys.stdout.write('%s\t%s\n'%(ss[0],'\t'.join(out)))

            except ValueError:
                sys.stderr.write('WARNING: parse value error, skip one line: %s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
