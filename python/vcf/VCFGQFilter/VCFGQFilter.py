#!/usr/bin/env python3

"""

    Filter genotype based on sample GQ values.

    @Author: wavefancy@gmail.com

    Usage:
        VCFGQFilter.py --mingq int
        VCFGQFilter.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, mask genotype as missing if GQ < 'mingq'.
        2. With support multiple allelic sites.
        3. Output results to stdout.
        4. Ignore the filter if the site call is already missing,  
               will not count into the final summary.

    Options:
        --mingq int     Minimum value for GQ, int.
                            Mask genotype as missing if GQ value  < 'mingq'.
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
    
    mingq = int(args['--mingq'])

    # API and example
    # https://brentp.github.io/cyvcf2/
    # https://brentp.github.io/cyvcf2/docstrings.html#api
    invcf = VCF('/dev/stdin', lazy=True, gts012=True)
    # invcf = VCF('test.vcf.gz', lazy=True)
    
    # adjust the header to contain the new field
    # the keys 'ID', 'Description', 'Type', and 'Number' are required.
    invcf.add_filter_to_header({'ID': 'VCFGQFilter.py', 
        'Description': 'Mask genotype as missing if GQ value  < '+str(mingq)})

    # create a new vcf Writer using the input vcf as a template.
    # Only need to write out updated VCF header.
    # Other parts output as string.
    sys.stdout.write('%s'%(invcf.raw_header))
    # outvcf = Writer('/dev/stdout', invcf)
    # outvcf.close()
    
    # Cache data for faster process.
    DATA_COL = 9
    FMT_COL  = 8
    FMT_STRING_CACHE = ''
    DP_COL = -1
    TOTAL_MAKSED = 0
    TOTAL_RECORDS = 0

    # Check this for each variants, avoid format change.
    def updateDPCOL(FMT_STRING):
        global FMT_STRING_CACHE, DP_COL
        if FMT_STRING != FMT_STRING_CACHE:
            try:
                DP_COL = FMT_STRING.strip().split(':').index('GT')
            except ValueError:
                sys.stderr.write('ERROR: can not find GT tag in FORMAT, %s\n'%(FMT_STRING))
                sys.exit(-1)
            FMT_STRING_CACHE = FMT_STRING
    
    def maskRecord(RECORD_ARRAY, INDEX):
        '''
            Mask a sample vcf GT as missing. Given an VCF variant array, and the index for change.
        '''
        ss = RECORD_ARRAY[INDEX].strip().split(':')
        ss[DP_COL] = './.'
        RECORD_ARRAY[INDEX] = ':'.join(ss)

    for variant in invcf:
        # This is the sum of gt_ref_depths + gt_alt_depths, check the code.
        # And confirmed by experiment.
        gq = variant.gt_quals

        # gt_types is array of 0,1,2,3==HOM_REF, HET, HOM_ALT, UNKNOWN
        gt_types = variant.gt_types

        # print(dp)
        ss = str(variant).split()
        updateDPCOL(ss[FMT_COL])

        TOTAL_RECORDS += (len(ss)-DATA_COL)

        # shift to the right pos for mask the genotype.
        # Only apply to the filter to the call the genotype is non-missing.
        min_mask_pos = np.nonzero(np.logical_and(gq < mingq, gt_types!=3))[0] + DATA_COL
        [maskRecord(ss, x) for x in min_mask_pos]
        TOTAL_MAKSED += min_mask_pos.size
        
        # Finished genotype updates.
        sys.stdout.write('%s\n'%('\t'.join(ss)))

    # sys.stderr.write('VCFGQFilter.py: '+'TOTAL MASKED RECORDS: %d\n'%(TOTAL_MAKSED))
    sys.stderr.write('VCFGQFilter.py: ' + 'TOTAL MASKED RECORDS: %d, of TOTAL: %d, Rate: %g\n'%(TOTAL_MAKSED, TOTAL_RECORDS,TOTAL_MAKSED*1.0/TOTAL_RECORDS))
    
    invcf.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
