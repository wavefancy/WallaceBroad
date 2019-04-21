#!/usr/bin/env python3

"""

    Count the number of alt alleles each vcf all.

    @Author: wavefancy@gmail.com

    Usage:
        VCF2AltCount.py
        VCF2AltCount.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin.
        2. Output results to stdout.
        3. Mising was imputed as ref.

    Options:
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
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    from pysam import VariantFile


    vcfMetaCols=9       #number of colummns for vcf meta information.
    tags = set(['GT'])

    def getGeno(geno):
        '''get genotype info. impute missing to ref.'''
        if geno[0] == '.': # if complete missing, output to ref.
            geno = '0/0'
        else:
            ss = geno.split(':')
            try:
                geno = ss[outGenoArrayIndex[0]]
            except IndexError:
                sys.stderr.write('ERROR: Index out of range. geno: %s, out index: %s\n'%(geno, str(outGenoArrayIndex)))
                sys.exit(-1)

        #set missing value to ref.
        geno = list(geno) # str to list.
        # expand x chromosome to homo. the genotye on chrX were coded as 0 or 1 as one haplotype, not two haplotypes.
        if len(geno) ==1:
            geno = [geno[0],'/',geno[0]]

        geno[0] = '0 ' if geno[0] == '.' else geno[0]
        geno[2] = '0' if geno[2] == '.' else geno[2]

        return geno

    outGenoArrayIndex = []
    def setoutGenoArrayIndex(oldFormatTags):
        '''Check and set the tag index based in input format string.'''
        outGenoArrayIndex.clear()
        ss = oldFormatTags.upper().split(':')
        for i in range(len(ss)):
            if ss[i] in tags:
                outGenoArrayIndex.append(i)

        if not outGenoArrayIndex:
            sys.stderr.write('ERROR: can not find tag: GT, from input vcf FORMAT field.\n'%(x))
            sys.exit(-1)

    def outputALTCount(ss):
        '''
            Count the the number of alt allels and output
        '''
        out = ss[:vcfMetaCols]
        allels = []
        for x in ss[vcfMetaCols:]:
            genotye = getGeno(x) # in standard format.
            count = 0
            if genotye[0] != '0':
                count += 1
            if genotye[2] != '0':
                count += 1
            out.append('%d'%(count))

        sys.stdout.write('%s\n'%('\t'.join(out)))

    infile = VariantFile('-', 'r')
    sys.stdout.write(str(infile.header))
    for line in infile:
        ss = str(line).strip().split()
        # find the GT tag position.
        setoutGenoArrayIndex(ss[8])
        # convert genotype to alt count.
        outputALTCount(ss)

    infile.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
