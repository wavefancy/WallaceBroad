#!/usr/bin/env python3

"""

    Aggregate/weight the number of rare variant in each individual.

    @Author: wavefancy@gmail.com

    Usage:
        RareVariantAggregator.py -w file
        RareVariantAggregator.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, and output results to stdout.
        2. Sum(rare_genone * weight)_across the whole input file.
            *** 0/0 and missing set genotype value of 0.
                non-0/0 set value of 1.
        3. The first field of FORMAT should be GT.

    Options:
        -w file         SNP weight file, two colummns, snpID and weight.
        -h --help       Show this screen.
        -v --version    Show version.
        -f --format     Show format example.
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
    args = docopt(__doc__, version='1.1')
    # version 1.1
    # Check format at each line. FORMAT may different line by line.
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    refGValue       =   0   #ref genotype value.
    nonRefGValue    =   1   #non-ref genotype value.
    vcfDataCol      =   9   #vcf data colummns.
    vcf_id_column   =   2   #vcf id colummns.

    #loading weight
    snp_weight = dict()
    with open(args['-w'], 'r') as wfile:
        for line in wfile:
            line = line.strip()
            if line:
                ss = line.split()
                if ss[0] not in snp_weight:
                    snp_weight[ss[0]] = float(ss[1])
                else:
                    sys.stderr.write('WARN: duplicate entry, snp this record: %s\n'%(line))

    def getGvalue(genotype):
        '''Convert genotype to value'''
        if genotype[0] == '.':
            return 0
        elif genotype[0] == '0' and genotype[2] == '0':
            return 0
        else:
            return 1

    #load input
    title  = []
    values = []
    indata = False
    for line in sys.stdin:
        line = line.strip()
        if line:
            if indata:
                ss = line.split()
                snpID = ss[vcf_id_column]
                if snpID not in snp_weight:
                    sys.stderr.write('ERROR: can not find weight for snp: %s\n'%(snpID))
                    sys.exit(-1)
                else:
                    weight = snp_weight[snpID]
                    snps   = ss[vcfDataCol:]
                    for i in range(len(values)):
                        values[i] += weight * getGvalue(snps[i])

            elif line.startswith('#CHROM'):
                ss = line.split()
                title = ss[vcfDataCol:]
                values = [0 for x in title]
                indata = True

    #output results
    for x,y in zip(title, values):
        sys.stdout.write('%s\t%.4e\n'%(x,y))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
