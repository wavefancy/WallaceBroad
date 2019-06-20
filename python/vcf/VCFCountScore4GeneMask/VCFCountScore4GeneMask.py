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
        --version        Show version.
        -f --format      Show format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
from cyvcf2 import VCF
from collections import OrderedDict
import numpy as np
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
    MAX_MAF = max(mafs)

    # gts012: bool
    #    if True, then gt_types will be 0=HOM_REF, 1=HET, 2=HOM_ALT, 3=UNKNOWN. If False, 3, 2 are flipped.
    # strict_gt: True: half missing set as UNKNOWN. Otherwise half missing set at HET.
    # API: https://brentp.github.io/cyvcf2/docstrings.html#api
    if samples: #automatic substract the subset of samples we want.
        vcf = VCF(vcf_file, gts012=True, strict_gt=True, samples=samples, lazy=True)
    else:
        vcf = VCF(vcf_file, gts012=True, strict_gt=True, lazy=True)

    # print(vcf.samples)
    out = "#CHROM  BEGIN   END     MARKER_ID       NUM_ALL_VARS    NUM_PASS_VARS   NUM_SING_VARS MAF_CUT".split()
    sys.stdout.write('%s\n'%('\t'.join(out + vcf.samples)))
    # go through the group file and count the scores.
    with open(group_file, 'r') as gfile:

        for line in gfile:
            line = line.strip()
            if line: # for each gene
                ss = line.split()
                # record weight map
                NUM_ALL_VARS = 0  # the number of sites defined in group file, but also found in vcf file.
                record_weight = {}
                positions = []
                for snp in ss[1:]:
                    t = snp.split(':')
                    key = ':'.join(t[:4])
                    w = float(t[4]) if len(t) == 5 else 1.0
                    record_weight[key] = w
                    positions.append(int(t[1]))

                # results for different MAFs.
                MAF_RESULTS = OrderedDict()
                MAF_RESULTS_PASS = OrderedDict()
                MAF_RESULTS_SING = OrderedDict()
                for x in mafs:
                    MAF_RESULTS[str(x)] = np.zeros(len(vcf.samples))
                    MAF_RESULTS_PASS[str(x)] = 0
                    MAF_RESULTS_SING[str(x)] = 0

                chr  = ss[1].split(':')[0]
                minp, maxp = (min(positions), max(positions))
                out = [chr, str(minp), str(maxp), ss[0]]
                # print(record_weight)
                # iterate through variant
                query = '%s:%d-%d'%(chr, minp, maxp)
                for variant in vcf(query): # query in a gene region.
                    # e.g. REF='A', ALT=['C', 'T']
                    # convert position from 0 based to 1 based.
                    # print(variant.start+1)
                    # print(variant.ALT)
                    ALT_ALLELE = variant.ALT[0] if variant.ALT else '.'
                    id = '%s:%s:%s:%s'%(variant.CHROM, variant.start+1, variant.REF, ALT_ALLELE)
                    # print(id)
                    if id in record_weight:
                        # print(id)
                        NUM_ALL_VARS += 1
                        aaf = variant.aaf # alt allele frequency across samples in this VCF.
                        v_maf = min(aaf, 1-aaf)
                        if v_maf == 0: continue # I don't think this kind of sites make sense for testing.
                        weight = np.power(1/(aaf * (1-aaf)),0.5) if weight_way == 'maf' else record_weight[id]

                        # filter by maf and do computation:
                        if v_maf <= MAX_MAF:
                            # gt_types is array of 0,1,2,3==HOM_REF, HET, UNKNOWN, HOM_ALT
                            genos = variant.gt_types
                            alt_count = variant.num_het + variant.num_hom_alt*2
                            # impute missing as HOM_REF
                            genos[genos == 3] = 0
                            # convert geno count to weight
                            genos = genos * weight
                            #genos[genos >0 ] *= weight

                            # aggregate results
                            for maf in mafs:
                                if v_maf <= maf:
                                    aid = str(maf)
                                    MAF_RESULTS_PASS[aid] = MAF_RESULTS_PASS[aid] + 1
                                    MAF_RESULTS[aid]      = MAF_RESULTS[aid] + genos

                                    if alt_count == 1:
                                        MAF_RESULTS_SING[aid] = MAF_RESULTS_SING[aid] + 1


                # print(MAF_RESULTS)
                #output results
                for maf in mafs:
                    aid = str(maf)
                    myout = out + [str(NUM_ALL_VARS), str(MAF_RESULTS_PASS[aid]), str(MAF_RESULTS_SING[aid]), aid] + ['%g'%(x) for x in MAF_RESULTS[aid]]

                    sys.stdout.write('%s\n'%('\t'.join(myout)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
