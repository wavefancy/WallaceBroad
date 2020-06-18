#!/usr/bin/env python3

"""

    Compute the missing rate of AD and DP field conditioned on a GQ threshold.

    @Author: wavefancy@gmail.com

    Usage:
        VCF_AD_DP_MissingByGQ.py [--minGQ int]
        VCF_AD_DP_MissingByGQ.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, output the results to stdout.

    Options:
        --minGQ int     The minimal GQ values to include [20].
        -h --help       Show this screen.
        -v --version    Show version.
        -f --format     Show format example.
"""
import sys
from docopt import docopt
from cyvcf2 import VCF, Writer
from collections import OrderedDict
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    ''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)
    
    minGQ = int(args['--minGQ']) if args['--minGQ'] else 20
    # API and example
    # https://brentp.github.io/cyvcf2/
    # https://brentp.github.io/cyvcf2/docstrings.html#api
    invcf = VCF('/dev/stdin', lazy=True, gts012=True)
    # invcf = VCF('test.vcf.gz', lazy=True)


    sys.stdout.write('GQ\tTOTAL\tDP_MISSING\tDP_MISSING_RATE\tAD_MISSING\tAD_MISSING_RATE\n')
    
    total_non_missing_ad = 0
    total                = 0
    total_non_missing_dp = 0

    for variant in invcf:
        ads = np.sum(variant.format('AD'),axis=1)
        dps = variant.format('DP').flatten()
        gqs = variant.format('GQ').flatten()
        # Select element meets good GQ values. missing is negative values.
        is_gq_good       = gqs >= minGQ
        is_gq_good_index = np.nonzero(is_gq_good)[0]
        # Subset to the elements with good GQ.
        ads = ads[is_gq_good_index]
        dps = dps[is_gq_good_index]

        total += is_gq_good_index.size
        total_non_missing_ad += np.sum(ads>0)
        total_non_missing_dp += np.sum(dps>0)

    # convert non-missing to missing count.
    dpm = total - total_non_missing_dp
    adm = total - total_non_missing_ad
    out = [minGQ, total, dpm, dpm/total, adm, adm/total]
    sys.stdout.write('%s\n'%('\t'.join(['%g'%(x) for x in out])))        
    invcf.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
