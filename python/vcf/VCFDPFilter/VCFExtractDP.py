#!/usr/bin/env python3

"""

    Extract the information from the AD field.

    @Author: wavefancy@gmail.com

    Usage:
        VCFExtractDP.py (-t | -a | -r)
        VCFExtractDP.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, output the results to stdout.
        2. With support multiple allelic sites.
        3. Output results to stdout.

    Options:
        -t              Extract the total read depth, sum of AD field.
        -a              Extract the alt allele read depth.
        -r              Extract the ref allele read depth.
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
    
    # API and example
    # https://brentp.github.io/cyvcf2/
    # https://brentp.github.io/cyvcf2/docstrings.html#api
    invcf = VCF('/dev/stdin', lazy=True, gts012=True)
    # invcf = VCF('test.vcf.gz', lazy=True)

    # create a new vcf Writer using the input vcf as a template.
    # Only need to write out updated VCF header.
    # Other parts output as string.
    # sys.stdout.write('%s'%(invcf.raw_header))
    # outvcf = Writer('/dev/stdout', invcf)
    # outvcf.close()
    sys.stdout.write('CHROM\tPOS\tREF\tALT\t%s\n'%('\t'.join(invcf.samples)))
    
    for variant in invcf:
        # This is the sum of gt_ref_depths + gt_alt_depths, check the code.
        # And confirmed by experiment.
        # Missing was coded as negative values.
        # dp = variant.gt_depths
        # rdp = variant.gt_ref_depths
        # adp = variant.gt_alt_depths
        # The above code do not support multi-allelic sites.
        # We support multi-allelic sites as below.

        dparray = variant.format('AD')
        # set missing (negative value) to as 0.
        dparray[dparray<0] = 0
        # get the total, alt and ref depth.

        # Convert from 0 based to 1 based.
        out = [variant.CHROM, str(variant.start+1), variant.REF, ','.join(variant.ALT)]
        np.set_printoptions(threshold=sys.maxsize,linewidth=sys.maxsize)
        if args['-t']:
            dp = np.sum(dparray,axis=1)
        if args['-a']:
            dp = np.sum(dparray[:,1:],axis=1)
        if args['-r']:
            dp = dparray[:,0]

        print('%s\t%s'%('\t'.join(out),np.array2string(dp,separator='\t')[1:-1]))
        
    invcf.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
