#!/usr/bin/env python3

'''

    Reweight the beta effect size based on a difference measure (d in [0,1]).
        The weight function is y = d^a, a in [0,20]

    @Author: wavefancy@gmail.com, Wallace Wang.

    Usage:
        CAPRSBetaReweighter.py -b int -d int -a vals [-m txt]
        CAPRSBetaReweighter.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. Add additional columns for the reweight beta by parameter a.

    Options:
        -b int        Column index for the beta value (int, 1 based).
        -d int        Column index for the difference measure, values usually in [0,1].
        -a vals       The parameter values for the weight function,
                          Suggest values in the interval of [0-20], eg. 0,0.1,3,20.
        -m txt        Set added value for entries don't have have a valid `-d` value, 
                          Default [0].
        -h --help     Show this screen.
        --version     Show version.
        -f --format   Show input/output file format example.

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.
from docopt import docopt

def ShowFormat():
    '''File format example'''
    print('''
#Input file format(stdin)
------------------------
RSID    BETA    A1      D
R1      1       A       0.1
R2      2       G       0.9

#cat test.txt | python ./CAPRSBetaReweighter.py -b 2 -d 4 -a 0.1,1,2
------------------------
RSID    BETA    A1      D       a_0.1       a_1     a_2
R1      1       A       0.1     0.794328    0.1     0.01
R2      2       G       0.9     1.97904     1.8     1.62
''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    Beta_COL  = int(args['-b']) -1
    Diff_COL  = int(args['-d']) -1 
    VALS      = [float(x) for x in args['-a'].split(',')]
    MVAL      = args['-m'] if args['-m'] else '0'

    TITLES    = ['a_%g'%(x) for x in VALS]
    MVALs     = [MVAL] * len(TITLES)
    FirstHit  = True

    for line in sys.stdin:
        line = line.strip()
        if line :
            ss = line.split()

            try:
                beta = float(ss[Beta_COL])
                diff = float(ss[Diff_COL])

                out = ss + ['%g'%(beta * pow(diff,x)) for x in VALS]
            except:
                if FirstHit:
                    out = ss + TITLES
                    FirstHit = False
                else:
                    out = ss + MVALs

            sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
