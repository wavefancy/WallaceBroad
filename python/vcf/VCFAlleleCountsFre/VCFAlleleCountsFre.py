#!/usr/bin/env python3

"""

    Count the number of alleles for VCF.

    ref, alt allele count, and alt allele frequency.

    @Author: wavefancy@gmail.com

    Usage:
        VCFAlleleCountsFre.py [-c txt]
        VCFAlleleCountsFre.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin.
        2. Output results to stdout.
        3. TotalCount: total non-missing ref+alt count.

    Options:
        -c txt          Specify statistics to calculate,
                          default: ALT_FRE: calculate alt allele frequency.
                           option: GP_GENO: genotype count based on imputation GP.
        -h --help       Show this screen.
        -v --version    Show version.
        -f --format     Show format example.
"""
import sys
from docopt import docopt
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
#CHROM  POS     REF     ALT     TotalCount      AltCount        AltFre
chr1    13273   G       T       4       4       1.0000
chr1    13289   CCT     C       4       0       0.0000
chr1    13417   C       CGAGA   2       2       1.0000
chr1    13649   G       C       4       1       0.2500
chr2    13649   G       C       4       1       0.2500
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    from pysam import VariantFile


    vcfMetaCols=9       #number of colummns for vcf meta information.
    tags = ['GT']
    OUT_FORMAT = 'ALT_FRE'
    if args['-c'] and args['-c'] not in ['ALT_FRE', 'GP_GENO']:
        sys.stderr.write('PLEASE set a proper value for "-c"!\n')
        sys.exit(-1)

    if args['-c'] == 'GP_GENO':
        OUT_FORMAT = 'GP_GENO'
        tags = ['GP']
        sys.stdout.write('#CHROM\tPOS\tREF\tALT\tCOUNT_0/0\tCOUNT_0/1\tCOUNT_1/1\n')

    if OUT_FORMAT == 'ALT_FRE':
        sys.stdout.write('#CHROM\tPOS\tREF\tALT\tTotalCount\tAltCount\tAltFre\n')

    def getGeno(geno):
        '''get genotype info.'''
        if geno[0] == '.':
            return './.'
        else:
            ss = geno.split(':')
            try:
                return ss[outGenoArrayIndex[0]]
            except IndexError:
                sys.stderr.write('ERROR: Index out of range. geno: %s, out index: %s\n'%(geno, str(outGenoArrayIndex)))
                sys.exit(-1)

    outGenoArrayIndex = []
    def setoutGenoArrayIndex(oldFormatTags):
        '''Check and set the tag index based in input format string.'''
        outGenoArrayIndex.clear()
        ss = oldFormatTags.upper().split(':')
        for x in tags:
            try:
                y = ss.index(x)
                outGenoArrayIndex.append(y)
            except ValueError:
                sys.stderr.write('ERROR: can not find tag: "%s", from input vcf FORMAT field.\n'%(x))
                sys.exit(-1)

    def outputAlleleFrequency(ss):
        '''Output allele frequency, in the format of:
            #CHROM  POS     REF     ALT     TotalCount      AltCount        AltFre
        '''
        out = ss[0:2] + ss[3:5]
        allels = []
        for x in ss[vcfMetaCols:]:
            genotye = getGeno(x)
            if genotye[0] != '.':
                allels.append(genotye[0])
            if genotye[2] != '.':
                allels.append(genotye[2])

        alt = 0
        ref = 0
        for x in allels:
            if x == '0':
                ref += 1
            else:
                alt += 1

        if alt + ref == 0:
            sys.stdout.write('%s\t%d\t%d\tNA\n'%('\t'.join(out), ref+alt, alt))
        else:
            sys.stdout.write('%s\t%d\t%d\t%.4f\n'%('\t'.join(out), ref+alt, alt, alt*1.0/(alt + ref)))

    def outputGPGenotype(ss):
        '''output genotype frequency based on imputation GP tag'''
        out = ss[0:2] + ss[3:5]
        values = []
        for x in ss[vcfMetaCols:]:
            values.append([float(t) for t in getGeno(x).split(',')])

        count = np.sum(np.array(values), axis=0)
        [out.append('%.3f'%(x)) for x in count]
        sys.stdout.write('%s\n'%('\t'.join(out)))

    infile = VariantFile('-', 'r')
    #sys.stdout.write(str(infile.header))
    for line in infile:
        ss = str(line).strip().split()
        setoutGenoArrayIndex(ss[8])

        if OUT_FORMAT == 'ALT_FRE':
            outputAlleleFrequency(ss)
        elif OUT_FORMAT == 'GP_GENO':
            outputGPGenotype(ss)

    infile.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
