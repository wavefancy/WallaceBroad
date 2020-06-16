#!/usr/bin/env python3

"""

    Filter HET genotype based on sample minor reads ratio.
    Minor-read ratio (MRR), which was defined as the ratio of reads for the less
    covered allele (reference or alt allele) over the total number of reads
    covering the position at which the variant was called. (Only applied to HET sites.)


    @Author: wavefancy@gmail.com

    Usage:
        VCFHETMinorReadsRatioFilter.py -c cutoff
        VCFHETMinorReadsRatioFilter.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, mask the genotype as missing if the MRR <  'cutoff'.
        2. With support multiple allelic sites.
        3. Output results to stdout.

    Options:
        -c cutoff       Mask the genotype as missing if the MRR <  'cutoff'.
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
    
    MRR_THRESHOLD = float(args['-c']) # the threshold minor reads ratio.

    # API and example
    # https://brentp.github.io/cyvcf2/
    # https://brentp.github.io/cyvcf2/docstrings.html#api
    invcf = VCF('/dev/stdin', lazy=True, gts012=True)
    # invcf = VCF('test.vcf.gz', lazy=True)
    
    # adjust the header to contain the new field
    # the keys 'ID', 'Description', 'Type', and 'Number' are required.
    invcf.add_filter_to_header({'ID': 'VCFHETMinorReadsRatioFilter', 
        'Description': 'Mask the genotype as missing if the MRR <  ' + args['-c']})
    
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
        ss[DP_COL] = '.'
        RECORD_ARRAY[INDEX] = ':'.join(ss)

    for variant in invcf:
        # print(variant.start+1)
        #This is the sum of gt_ref_depths + gt_alt_depths, checked the code.
        rdp = variant.gt_ref_depths #ref depth
        adp = variant.gt_alt_depths #alt depth
        tdp = variant.gt_depths     #ref + alt.
        alt_count = variant.gt_types # HOM_REF=0, HET=1. For gts012=True HOM_ALT=2, UKNOWN=3
        # print(rdp)
        # print(adp)
        # print(alt_count)

        # apply the filter only on het sites.
        is_het = alt_count == 1
        # to avoid site has total dp as 0, devided by zero thereafter.
        is_het = np.logical_and(is_het, tdp >0)

        is_het_index = np.nonzero(is_het)[0]
        alt_ratio = adp[is_het]/tdp[is_het]
        mrr_ratio = np.minimum(alt_ratio, 1-alt_ratio)
        mask_pos = is_het_index[mrr_ratio < MRR_THRESHOLD]
        if mask_pos.size == 0: # no update, no split and combine.
            sys.stdout.write(str(variant))
            continue

        TOTAL_MAKSED += mask_pos.size
        # print(is_het_index)
        # print(mrr_ratio)
        # print(mask_pos)

        # gt_ref_depths is from the 'AD' field.
        ss = str(variant).split()
        updateDPCOL(ss[FMT_COL])

        # shift to the right pos for mask the genotype.
        mask_pos = mask_pos + DATA_COL
        [maskRecord(ss, x) for x in mask_pos]
        sys.stdout.write('%s\n'%('\t'.join(ss)))
        
    sys.stderr.write('VCFHETMinorReadsRatioFilter.py: ' + 'TOTAL MASKED RECORDS: %d\n'%(TOTAL_MAKSED))
    invcf.close()
    # outvcf.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
