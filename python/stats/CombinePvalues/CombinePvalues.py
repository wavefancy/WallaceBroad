#!/usr/bin/env python3

"""

    Combine multiple pvalues.
    @Author: wavefancy@gmail.com

    Usage:
        CombinePvalues.py -k indexs [-s] [-t threshold]
        CombinePvalues.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin and output results to stdout, add one column for combined pvalue.
        2. See example by -f.

    Options:
        -k indexs      Column index for input pvalues, eg 1,2|1,3,4.
        -t threshold   Pvalue threshold to be included in combined pvalue,
                       eg. 0.05,1 | 1,1,0.005.
                       Only pvalue less than this threshold will be combined, otherwise set as 1.
                       The number of values set here should be the same as -k parameter.
        -s             Specify use 'stouffer' method for combine, default 'fisher' method.
        -h --help      Show this screen.
        -v --version   Show version.
        -f --format    Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def ShowFormat():
    '''Input File format example:'''
    print('''
# input example:
# echo -e '0.5 0.1\\n2.8784e-21 8.6420e-01\\n8.7935e-04 5.8147e-04' | python3 CombinePvalues.py -k 1,2 -s
--------------------------
0.5	0.1	1.8242e-01
2.8784e-21	8.6420e-01	2.2398e-09
8.7935e-04	5.8147e-04	3.2638e-06

#==========================================
#echo -e '0.5 0.1\\n2.8784e-21 8.6420e-01\\n8.7935e-04 5.8147e-04' | python3 CombinePvalues.py -k 1,2 -s -t 0.05,0.1
0.5     0.1     1.0000e+00
2.8784e-21      8.6420e-01      1.0000e+00
8.7935e-04      5.8147e-04      3.2638e-06
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    pvindex = [int(x)-1 for x in args['-k'].split(',')]
    pthreshold = [1 for x in pvindex]
    if args['-t']:
        pt = [float(x) for x in args['-t'].split(',')]
        if len(pt) != len(pthreshold):
            sys.stderr.write('The number of parameter for -t is different with -k, please check !\n')
            sys.exit(-1)
        else:
            pthreshold = pt

    method = 'fisher'
    if args['-s']:
        method = 'stouffer'

    from scipy import stats
    #api: print(stats.binom_test.__doc__)
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                ipv = [float(ss[i]) for i in pvindex]
                # checking threshold.
                incombine = True
                for x, y in zip(ipv, pthreshold):
                    if x > y:
                        ss.append('%.4e'%(1))
                        incombine = False
                        break

                if incombine:
                    pv = stats.combine_pvalues(ipv, method=method)
                    #print(pv)
                    ss.append('%.4e'%(pv[1]))
            except ValueError:
                ss.append('CombinedPValue')

            sys.stdout.write('%s\n'%('\t'.join(ss)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
