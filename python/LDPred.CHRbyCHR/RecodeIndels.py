#!/usr/bin/env python3

'''

    Recode indels as A/G, as LDpred will ignore indels.
    It defines the validation allele as: valid_nts = set(['A','T','C','G'])
    Short allele recode as A, longer allele recode as G.

    @Author: wavefancy@gmail.com, Wallace Wang.

    Usage:
        RecodeIndels.py -a ints -b ints
        RecodeIndels.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.

    Options:
        -a ints       Column index for alleles for data set1, eg. 1,2.
        -b ints       Column index for alleles for data set2, eg. 3,4.
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
AA      T       AA      T
A       TT      A       TT
A       G       A       G
A       G       A       K
AA      T       T       AA

cat test.recode.txt | python3 RecodeIndels.py -a 1,2 -b 3,4
------------------------
G       A       G       A
A       G       A       G
A       G       A       G
A       G       A       K
G       A       A       G

          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    col_a = [int(x)-1 for x in args['-a'].split(",")]
    col_b = [int(x)-1 for x in args['-b'].split(",")]

    for line in sys.stdin:
        line = line.strip()
        if line :
            ss = line.split()

            allele_len = [len(ss[x]) for x in col_a + col_b]
            if sum(allele_len) != 4: # try recoding.
                if ss[col_a[0]] == ss[col_b[0]] and ss[col_a[1]] == ss[col_b[1]]:
                    if len(ss[col_a[0]])<len(ss[col_a[1]]):
                        ss[col_a[0]] = 'A'
                        ss[col_a[1]] = 'G'
                        ss[col_b[0]] = 'A'
                        ss[col_b[1]] = 'G'
                    else:
                        ss[col_a[0]] = 'G'
                        ss[col_a[1]] = 'A'
                        ss[col_b[0]] = 'G'
                        ss[col_b[1]] = 'A'

                    sys.stdout.write('%s\n'%('\t'.join(ss)))
                elif ss[col_a[0]] == ss[col_b[1]] and ss[col_a[1]] == ss[col_b[0]]:
                    if len(ss[col_a[0]])<len(ss[col_a[1]]):
                        ss[col_a[0]] = 'A'
                        ss[col_a[1]] = 'G'
                        ss[col_b[0]] = 'G'
                        ss[col_b[1]] = 'A'
                    else:
                        ss[col_a[0]] = 'G'
                        ss[col_a[1]] = 'A'
                        ss[col_b[0]] = 'A'
                        ss[col_b[1]] = 'G'

                    sys.stdout.write('%s\n'%('\t'.join(ss)))
                else: #failed matching, skipping.
                    sys.stdout.write('%s\n'%(line))
            else:
                sys.stdout.write('%s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
