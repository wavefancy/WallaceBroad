#!/usr/bin/env python3

"""

    Corrdinate GWAS effect size (beta). Align to the same reference(Effective) allele.
    1. Switch the second effective allele, and then covert the second beta to -1.0 * beta.
    2. Take care strand flip issue.

    @Author: wavefancy@gmail.com

    Usage:
        AlignGWASBeta.py -a ints -b ints
        AlignGWASBeta.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. Switch effective allele and it's corrsponding effect size.
           Add one column for status.
        3. See example by -f.

    Options:
        -a ints       Column index for two GWAS alleles, e.g. 2,3,5,6
        -b ints       Column index for two GWAS betas, e.g. 4,7
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''

    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    # Column index for alleles
    a_col = [int(x)-1 for x in args['-a'].split(',')]
    # Column index for betas, only change the last one if possible.
    b_col = int(args['-b'].split(',')[-1])-1
    maxsplit = max(a_col + [b_col]) +1

    OutComment = True

    def checkAndOutput(ss, a_col, b_col):
        ''''Compare allels and output results.
            ss: input conent array.
            a_col: column index for alleles.
            b_col: column index for then second beta.
        '''
        alleles = [ss[x].upper() for x in a_col]

        alleles_left = alleles[:2]
        alleles_right = alleles[2:]

        if alleles_left == alleles_right:
            sys.stdout.write('%s\tOK\n'%('\t'.join(ss)))
            return True
        # switch effect allles.
        temp = [alleles_right[1],alleles_right[0]]
        if alleles_left == temp:
            ss[b_col] = str(-1.0 * float(ss[b_col]))
            ss[a_col[-2]] = temp[0]
            ss[a_col[-1]] = temp[1]
            sys.stdout.write('%s\tOK\n'%('\t'.join(ss)))
            return True

        return False

    flip_map = {'A':'T', 'T':'A', 'G':'C','C':'G', '0':'0', 'N':'N'}
    def flip(string):
        '''flipping strand, flip or keep the sample if the allele code is out-of-control.'''
        return ''.join([flip_map[x] for x in string])

    AT=['A', 'T']
    CG=['C', 'G']
    for line in sys.stdin:
        line = line.strip()
        if line:

            if OutComment and line.startswith('#'):
                sys.stdout.write('%s\n'%(line))
                continue

            ss = line.split(None, maxsplit)
            alleles = [ss[x].upper() for x in a_col]

            alleles_left = alleles[:2]
            alleles_right = alleles[2:]
            # check allele A/T, G/C allele.
            temp = sorted(alleles_left)
            if temp == AT or temp == CG:
                sys.stdout.write('%s\tAMBIGUOUS\n'%(line))
                continue

            if checkAndOutput(ss, a_col, b_col):
                continue

            # flip strand
            ss[a_col[-2]] = flip(ss[a_col[-2]])
            ss[a_col[-1]] = flip(ss[a_col[-1]])
            if checkAndOutput(ss, a_col, b_col):
                continue
            sys.stdout.write('%s\tFAIL\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
