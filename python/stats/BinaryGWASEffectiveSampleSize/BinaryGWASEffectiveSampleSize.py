#!/usr/bin/env python3

"""

    Estimate effective sample size for binary traits

    @Author: wavefancy@gmail.com

    Usage:
        BinaryGWASEffectiveSampleSize.py -t name1,name2 [-i]
        BinaryGWASEffectiveSampleSize.py -h | --help | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout.
        2. Add one column for the effective sample size estimation.

    Options:
        -t name1,name2  Column name for the sample size of case and control.
        -i              Force the output sample size estimation as INT.
        -h --help       Show this screen.
        --version       Show version.
        -f --format     Show input/output file format example.

    References:
        Effective sample size for binary gwas is: 4/(1/N_case + 1/N_control)
        1. https://www.nature.com/articles/ejhg2016150
        2. http://www.nealelab.is/blog/2017/9/20/insights-from-estimates-of-snp-heritability-for-2000-traits-and-disorders-in-uk-biobank#footnote3

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

def ShowFormat():
    '''Input File format example:'''
    print('''
# INPUT:
# ----------------------
 CASE CONTROL
 2 3
 3 2
 1 1
 10 20

# OUTPUT:
# cat test.txt | python ./BinaryGWASEffectiveSampleSize.py -t CASE,CONTROL
# ----------------------
CASE CONTROL    EffectiveSampleSize
2 3     4.8
3 2     4.8
1 1     2
10 20   26.6667
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    T_KEYS = [x for x in args['-t'].split(',')]
    if T_KEYS:
        WITH_TITLE = True
    if len(T_KEYS) !=2:
        sys.stderr.write('ERROR, please specify two columns separated by ","! YOUR INPUT: %s\n'%(args['-t']))
        sys.exit(-1)

    force_int = True if args['-i'] else False

    INDEXMAP = {}
    KEYS = []
    DELIMITER = None
    for line in sys.stdin:
        line = line.strip()
        if line:
            if WITH_TITLE:
                if T_KEYS:
                    ss = line.split()
                    for k,v in zip(ss, range(len(ss))):
                        if k in INDEXMAP:
                            sys.stderr.write('ERROR, Dupliciate values in title, -t model failed! DUP KEY: %s\n'%(k))
                            sys.exit(-1)
                        else:
                            INDEXMAP[k] = v
                    for k in T_KEYS:
                        if k not in INDEXMAP:
                            sys.stderr.write('ERROR, key not in title: %s\n'%(k))
                            sys.exit(-1)
                        else:
                            KEYS.append(INDEXMAP[k])
                    maxSplit = max(KEYS) + 2

                sys.stdout.write('%s\tEffectiveSampleSize\n'%(line))
                WITH_TITLE = False

            else:
                ss = line.split(DELIMITER, maxSplit)
                c1 = 1/(float(ss[KEYS[0]]))
                c2 = 1/(float(ss[KEYS[1]]))
                Neff = 4/(c1 + c2)

                if force_int:
                    sys.stdout.write('%s\t%d\n'%(line,Neff))
                else:
                    sys.stdout.write('%s\t%g\n'%(line,Neff))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
