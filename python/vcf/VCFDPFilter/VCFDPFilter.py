#!/usr/bin/env python3

"""

    Filter genotype based on sample total AD tag values (total read depth).

    @Author: wavefancy@gmail.com

    Usage:
        VCFDPFilter.py [--mindp int] [--maxdp int] [--field text]
        VCFDPFilter.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, mask genotype as missing if failed the filter.
        2. With support multiple allelic sites.
        3. Output results to stdout.

    Options:
        --mindp int     Minimum value for total AD tag(read depth), int.
                            Mask genotype as missing if total AD < 'mindp'.
        --maxdp int     Maximum value for total AD tag(read depth), int.
                             Mask genotype as missing if total AD > 'maxdp'.
        --field text    From which part the total reads depths were extracted.
                            DP|AD, [DP].
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
    
    minDP = int(args['--mindp'])     if args['--mindp'] else -1
    maxDP = int(args['--maxdp'])     if args['--maxdp'] else -1
    field = args['--field'].upper()  if args['--field'] else 'DP'
    if minDP < 0 and maxDP <0:
        sys.stderr.write('ERROR: please specify at least one option of "--mindp" or "--maxpd"\n')
        sys.exit(-1)

    # API and example
    # https://brentp.github.io/cyvcf2/
    # https://brentp.github.io/cyvcf2/docstrings.html#api
    invcf = VCF('/dev/stdin', lazy=True, gts012=True)
    # invcf = VCF('test.vcf.gz', lazy=True)
    
    # adjust the header to contain the new field
    # the keys 'ID', 'Description', 'Type', and 'Number' are required.
    if minDP >= 0:
        invcf.add_filter_to_header({'ID': 'VCFDPFilter.py', 
            'Description': 'Mask the genotype as missing if the total read depth (AD) < '+str(minDP)})
    if maxDP >= 0:
        invcf.add_filter_to_header({'ID': 'VCFDPFilter.py', 
            'Description': 'Mask the genotype as missing if the total read depth (AD) > '+str(maxDP)})
    
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
        ss[DP_COL] = './.'
        RECORD_ARRAY[INDEX] = ':'.join(ss)

    for variant in invcf:
        # This is the sum of gt_ref_depths + gt_alt_depths, check the code.
        # And confirmed by experiment.
        # dp = variant.gt_depths
        # rdp = variant.gt_ref_depths
        # adp = variant.gt_alt_depths
        if field == 'DP':
            dp = variant.format('DP').flatten() # convert to one row.
        else:
            # The above code do not support multi-allelic sites.
            # We support multi-allelic sites as below.
            dparray = variant.format('AD')
            # set missing (negative value) to as 0.
            dparray[dparray<0] = 0
            # total DP.
            dp = np.sum(dparray,axis=1)
 
        ss = str(variant).split()
        updateDPCOL(ss[FMT_COL])

        # shift to the wright pos for mask the genotype.
        if minDP > 0:
            # negative value already as missing, just skipped.
            min_mask_pos = np.nonzero(np.logical_and(dp < minDP, dp > 0))[0] + DATA_COL
            [maskRecord(ss, x) for x in min_mask_pos]
            TOTAL_MAKSED += min_mask_pos.size

        if maxDP > 0:
            max_mask_pos = np.nonzero(dp > maxDP)[0] + DATA_COL
            [maskRecord(ss, x) for x in max_mask_pos]
            TOTAL_MAKSED += max_mask_pos.size
        
        # Finished genotype updates.
        sys.stdout.write('%s\n'%('\t'.join(ss)))

    sys.stderr.write('VCFDPFilter.py: ' + 'TOTAL MASKED RECORDS: %d\n'%(TOTAL_MAKSED))
    invcf.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
