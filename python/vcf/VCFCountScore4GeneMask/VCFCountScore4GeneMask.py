#!/usr/bin/env python3

"""

    Aggregate/weight the number of rare variant in each individual in each gene.

    @Author: wavefancy@gmail.com

    Usage:
        VCFCountScore4GeneMask.py -g file -v bgzfile [--weight text] [-s file] --max-maf floats
        VCFCountScore4GeneMask.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Output to stdout, each line for each gene mask.
        2. *** Do not support multi-allelic sites in the current version.

    Options:
        -g file          Group file, each line is a group of variants.
        -v bgzfile       Bgziped and tabix indexed vcf file.
        --weight txt     The way for aggregate variant. Default: file.
                             file: sum(alt_count*variant_weight), variant_weight from group file.
                                   Set as 1 if group file don't have weight.
                             MAF:  Set the weight as 1/(MAF*(1-MAF))^0.5. Madsen and Browning (2009).
        -s file          Sample file, only count the score for those individuals decleared in this file.
        --max-maf floats MAF cut-off for variants, eg. 0.01|0.01,0.05
        -h --help        Show this screen.
        -v --version     Show version.
        -f --format      Show format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
from cyvcf2 import VCF
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

    group_file = args['-g']
    vcf_file = args['-v']
    weight_way = args['--weight'] if args['--weight'] else 'file'
    weight_way = weight_way.lower()
    if weight_way not in set(['file','maf']):
        sys.stderr.write('Please set a proper value for --weight')

    samples = []
    with open(args['-s'], 'r') as sfile:
        for line in sfile:
            line = line.strip()
            if line:
                ss = line.split()
                [samples.append(x) for x in ss]
    # convert list to set for fast checking
    # samples = set(samples)

    mafs = [float(x) for x in args['--max-maf'].split(',')]

    # gts012: bool
    #    if True, then gt_types will be 0=HOM_REF, 1=HET, 2=HOM_ALT, 3=UNKNOWN. If False, 3, 2 are flipped.
    # strict_gt: True: half missing set as UNKNOWN. Otherwise half missing set at HET.
    # API: https://brentp.github.io/cyvcf2/docstrings.html#api
    if samples:
        vcf = VCF(vcf_file, gts012=True, strict_gt=True, samples=samples)
    else:
        vcf = VCF(vcf_file, gts012=True, strict_gt=True)

    print(vcf.samples)
    # go through the group file and count the scores.
    with open(group_file, 'r') as gfile:
        for line in gfile:
            line = line.strip()
            if line:
                ss = line.split()
                # record weight map
                record_weight = {}
                positions = []
                for snp in ss[1:]:
                    t = snp.split(':')
                    key = ':'.join(t[:4])
                    w = float(t[4]) if len(t) == 5 else 1.0
                    record_weight[key] = w
                    positions.append(int(t[1]))

                chr  = ss[1].split(':')[0]
                # iterate through variant
                for variant in vcf('%s:%d-%d'%(chr, min(positions), max(positions
                    # e.g. REF='A', ALT=['C', 'T']
                    id = '%s:%s:%s:%s'%(variant.CHROM, variant.start, variant.REF, variant.ALT[0])
                    if id in record_weight:
                        aaf = v.aaf # alt allele frequency across samples in this VCF.
                        weight = (1/(aaf * (1-aaf)))^0.5 if weight_way == 'maf' else record_weight[id]

                        # filter by maf and do computation:
                        

                        # gt_types is array of 0,1,2,3==HOM_REF, HET, UNKNOWN, HOM_ALT
                        genos = v.gt_types
                        # impute missing as HOM_REF
                        genos[genos == 3] = 0
                        # convert geno count to weight
                        genos[genos >0 ] *= weight




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
