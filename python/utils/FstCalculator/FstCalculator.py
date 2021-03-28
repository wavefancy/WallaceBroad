#!/usr/bin/env python3

'''

    Calculate the Fst based on allele frequency and sample size.
        Fst = [S_t - sum(S_i)]/S_t, 
        The proportion of between group variance over the total variance.
        https://en.wikipedia.org/wiki/Fixation_index

        S_i = N_i * p_i * (1-p_i). N_t = sum(N_i). so the c_i is
        c_i = N_i/N_t.

    @Author: wavefancy@gmail.com, Wallace Wang.

    Usage:
        FstCalculator.py
        FstCalculator.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. The input format is MarkerID F1 N1 F2 N2 ...

    Options:
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
rsid    f1      n1      f2      n2      f3      n3
r1      0.5     100     0.5     100     0.5     100
r2      0.5     500     0.65    100     0.35    1000

cat test.txt | python ./FstCalculator.py 
rsid    Fst
------------------------
r1      0
r2      0.0343774
''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    TITLES    = ['Fst']

    for line in sys.stdin:
        line = line.strip()
        if line :
            ss = line.split()

            try:
                val = [float(x) for x in ss[1:]]
                Fi  = val[0::2]
                Ni  = val[1::2]

                Nt  = sum(Ni)
                Ci  = [x*1.0/Nt for x in Ni]
                Var_it = sum([x*y*(1-y) for x,y in zip(Ci, Fi)])
                Ft = sum([x*y for x,y in zip(Fi,Ni)])/Nt
                Var_t = Ft * (1-Ft)

                out = [ss[0]] + ['%g'%((Var_t-Var_it)/Var_t)]
            except:
                out = [ss[0]] + TITLES

            sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
