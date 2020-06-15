#!/usr/bin/env python3

"""

    Filter site based on the missingness across all samples.

    @Author: wavefancy@gmail.com

    Usage:
        VCFSiteMissingFilter.py -m float
        VCFSiteMissingFilter.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, exclude the site with missing rate higher than '-m'.
        2. With support multiple allelic sites.
        3. Output results to stdout.

    Options:
        -m float        The cut-off for site missingness.
                            Exclude sites with missing > '-m' value.
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
    
    MISS_THRESHOLD = float(args['-m'])

    # API and example
    # https://brentp.github.io/cyvcf2/
    # https://brentp.github.io/cyvcf2/docstrings.html#api
    invcf = VCF('/dev/stdin', lazy=True, gts012=True) # if gts012=True, then gt_types will be 0=HOM_REF, 1=HET, 2=HOM_ALT, 3=UNKNOWN. 
    # invcf = VCF('test.vcf.gz', lazy=True)
    
    # adjust the header to contain the new field
    # the keys 'ID', 'Description', 'Type', and 'Number' are required.

    invcf.add_filter_to_header({'ID': 'VCFSiteMissingFilter.py', 
        'Description': 'Exclude the site with missing rate higher than > '+str(MISS_THRESHOLD)})
    
    # create a new vcf Writer using the input vcf as a template.
    # Only need to write out updated VCF header.
    # Other parts output as string.
    outvcf = Writer('/dev/stdout', invcf)
    outvcf.close()
    
    for variant in invcf:
        missing_rate = 1 - variant.call_rate
        if missing_rate <= MISS_THRESHOLD:
            ss = str(variant).split()
            sys.stdout.write(str(variant))

    invcf.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
