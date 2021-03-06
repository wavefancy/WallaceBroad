#!/usr/bin/env python3

"""

    Transform the number of a column.
    @Author: wavefancy@gmail.com

    Usage:
        ColumnTransformator.py -c col -t transformer [-f text]
        ColumnTransformator.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -c col         Column (index|name) for transformer to be applied.
        -t transformer Transform action, name are case sensitive:
                       maf : to minor allele frequency. min(1-p,p)
                       nlog: negative log. val --> -1.0 * math.log10(float(val))
                       log: val -> math.log(val), log base as e.
                       nint: nearst int value.
                       subfrom1: val -> 1-val
                       plus1int: val -> val+1 (parse value as int, output also int, only work for int value.)
                       entropy: val -> -1*val*math.log10(val)
                       LODP: linkage LOD score to P value.
                       LODX2: linkage LOD score to chisq value, degree of one.
                       P2Z:sign_col: convert P value to Z score, assume the P value is two-sided P value.
                            'sign_col' (int or name), set the sign for Z score based on this column. 
                       format: apply the '-f' format pattern to the value.
        -f text        Format string for output, eg: %.4e| %.4f default: %g.
        -h --help      Show this screen.
        -v --version   Show version.
        --format    Show input/output file format example.
"""
import sys
from scipy import stats
import scipy as sp
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def ShowFormat():
    '''Input File format example:'''
    print('''
# Input
# -----------------
Z P ZfromP
1.25500e+01 3.97510e-36 3.97510e-36
-3.01130e+00 2.60132e-03 2.60132e-03

#  cat ./in.p2v.2sided.txt | python3 ./ColumnTransformator.py -c ZfromP -t P2Z:Z
# -----------------
Z       P       ZfromP
1.25500e+01     3.97510e-36     12.55
-3.01130e+00    2.60132e-03     -3.0113
    ''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    try:
        COL = int(args['-c']) -1
    except ValueError:
        # COL is as name not by index.
        COL = -1
    
    # ACTION = args['-t'].lower()
    ACTION = args['-t']
    FORMATS = args['-f'] if args['-f'] else '%g'

#### ***** Define the function map for transformer ****####
    # https://stackoverflow.com/questions/9168340/using-a-dictionary-to-select-function-to-execute
    # Dynamically define dictionary, map function.
    Transformers = {}
    trans = lambda f: Transformers.setdefault(f.__name__, f)
    @trans
    def maf(v):
        return FORMATS%(min(v, 1-v))
    @trans
    def nlog(v):
        t = -1.0 * math.log10(v); return FORMATS%(t)
    @trans
    def nint(v):
        t = int(float(v)+0.5 ); return '%d'%(t)
    @trans
    def subfrom1(val):
        return FORMATS%(1-val)
    @trans
    def plus1int(v):
        return '%d'%(v+1)
    @trans
    def entropy(v):
        return FORMATS%(-1*v*math.log10(v))
    @trans
    def log(val):
        return FORMATS%(math.log(val))
    @trans
    def P2Z(val, sign_val):
        # stats.norm.ppf is qnorm in R, working on left side below.
        v = sp.sign(sign_val) * -1.0 * stats.norm.ppf(val / 2.0)
        return FORMATS%(v)
    @trans
    def LODP(val):
        val = val * 4.6 # (2*ln10) = 4.6
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2.html
        # convert chi2 to P value.
        p = stats.chi2.sf(val, 1) / 2
        return FORMATS%(p)
    @trans
    def LODX2(val):
        val = val * 4.6 # (2*ln10) = 4.6
        return FORMATS%(val)
    @trans
    def format(val):
        return FORMATS%(val)
#### *****END Define the function map for transformer ****####

    if ACTION.split(':')[0] not in Transformers.keys():
        sys.stderr.write('Transformer "%s" is not supported! Please check!\n'%(ACTION))
        sys.exit(-1)

    import math
    from scipy import stats
    name_index_map = {}
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if COL < 0:
                # parse the title line and set an index map.
                for i,val in enumerate(ss):
                    if val in name_index_map:
                         sys.stderr.write('ERROR: duplicated key in title line: %s\n'%(val))
                    else:
                        name_index_map[val] = i
                COL = name_index_map[args['-c']]
            else:
                try:
                    if ACTION.startswith('P2Z'):
                        t = ACTION.split(':')
                        try:
                            sign_col = int(t[1])
                        except ValueError:
                            sign_col = name_index_map[t[1]]
                        ss[COL] = Transformers[t[0]](float(ss[COL]),float(ss[sign_col]))
                    else:
                        ss[COL] = Transformers[ACTION](float(ss[COL]))
                except ValueError:
                    sys.stderr.write('WARNING: Can not parse number in line: %s\n'%(line))
                    # ss[COL] = ACTION
            sys.stdout.write('%s\n'%('\t'.join(ss)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
