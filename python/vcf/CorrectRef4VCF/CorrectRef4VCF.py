#!/usr/bin/env python3

"""

    Check reference allele consistency for VCF file. And
    *** Try to correct inconsistent sites****
    @Author: wavefancy@gmail.com

    Usage:
        CorrectRef4VCF.py -r <ref.fa> [-c int]
        CorrectRef4VCF.py -h | --help | -v | --version | -f

    Notes:
        1. Read vcf file from stdin and output results to stdout.
        2. Reference index is 1 based. *** VCF input is 0 based.
        3. **** Only check biallelic sites, skip all the other sites in output.
            - Skip structure sites.
            - Skip sites with unrecognized alleles, alleles except [A,T,G,C].
              Like the vcf files converted back from plink files, many contain
              site with alt allele as '.', thie type of sites will be skipped
              from the output.
        4. Correct inconsistent sites, flipping strand if necessary.
        5. **** Only correct genotype, ignore other parts, like AD field.

    Options:
        -r FILE       Indexed(.fai) fasta Reference file.
        -c int        Change the preload ref cache size, default: 10,000,000.
        -h --help     Show this screen.
        -v --version  Show version.
        -f            Show format example.
    Dependency:
        pyfaidx: https://pypi.python.org/pypi/pyfaidx

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)
    if args['-f']:
        '''File format example'''
        print('''
#input vcf example:
------------------------
#CHROM  POS ID  REF ALT QUAL    FILTER  INFO    FORMAT  Sample_M_FG-NY14_006_006
chr1    1   .   G   A   111.66  PASS    .   GT:AD:DP:GQ:PL  0/0:31,0:31:78:0,78,1170
chr1    2   .   GGGT    G   85.53   PASS    .   GT:AD:DP:GQ:PL  0/0:34,0:34:81:0,81,1215
chr1    3   .   G   C   74.96   PASS    .   GT:AD:DP:GQ:PGT:PID:PL  0/0:36,0:36:99:.:.:0,99,1485
chr1    4   .   T   G   3319.08 PASS    .   GT:AD:DP:GQ:PL  0/0:44,0:44:99:0,99,1485
chr1    5  .   C   T   4145.15 PASS    .   GT:AD:DP:GQ:PGT:PID:PL  0/0:17,0:17:51:.:.:0,51,573
chr1    6  .   C   G   6211.15 PASS    .   GT:AD:DP:GQ:PGT:PID:PL  0/0:17,0:17:0:.:.:0,0,450
#input refGenome
------------------------
>chr1
AAGAAA
#output vcf.
------------------------
#CHROM  POS ID  REF ALT QUAL    FILTER  INFO    FORMAT  Sample_M_FG-NY14_006_006
chr1    1       .       A       G       111.66  PASS    .       GT:AD:DP:GQ:PL  1/1:31,0:31:78:0,78,1170
chr1    3       .       G       C       74.96   PASS    .       GT:AD:DP:GQ:PGT:PID:PL  0/0:36,0:36:99:.:.:0,99,1485
chr1    4       .       A       C       3319.08 PASS    .       GT:AD:DP:GQ:PL  0/0:44,0:44:99:0,99,1485
chr1    5       .       A       G       4145.15 PASS    .       GT:AD:DP:GQ:PGT:PID:PL  1/1:17,0:17:51:.:.:0,51,573
#output error.
------------------------
WARNING: Skip non-biallelic site: chr1  2       .       GGGT
WARNING: failed even after flipping strand: chr1        6       .       C       G
              ''');
        sys.exit(0)

    refFile = args['-r']
    seqStart = 9 #column idex for sequence start.

    from pyfaidx import Fasta
    read_ahead = int(args['-c']) if args['-c'] else 10000000
    refGenome = Fasta(refFile, sequence_always_upper=True,read_ahead=read_ahead)

    convertMap = {'0':'1','1':'0','.':'.'}
    def exchangeRefAlt(vcfLine):
        '''Exchange ref/alt representation of a vcf line
           Ref <---> alt
        '''
        ss = vcfLine
        #exchange ref/alt
        ss[3],ss[4] = ss[4],ss[3]
        for i in range(seqStart,len(ss)):
            ns = list(ss[i]) #convet string to list, string are immutable.
            ns[0] = convertMap[ns[0]]
            ns[2] = convertMap[ns[2]]
            # if ns[0] == '0':
            #     ns[0] = '1'
            # else: # value 1
            #     ns[0] = '0'
            #
            # if ns[2] == '0':
            #     ns[2] = '1'
            # else: # 1
            #     ns[2] = '0'

            ss[i] = ''.join(ns)
        return ss
    def getOutputArray(vcfLine, refAllele):
        '''Check consistency of a vcf line, exchange ref/alt if necessary.
           return corrected vcfLine, [] if exchange also failed.
        '''
        # print(refAllele)
        out = []
        ref = vcfLine[3].upper()
        alt = vcfLine[4].upper()
        if refAllele == ref:
            out = vcfLine
        elif refAllele == alt:
            out = exchangeRefAlt(vcfLine)
        else: #
            out = []
        return out

    flipMap = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
    #read input vcf file and check ref alleles.
    data = False
    for line in sys.stdin:
        line = line.strip()
        if line:
            if data:
                ss = line.split()
                if len(ss[3]) != 1 or len(ss[4]) != 1:
                    sys.stderr.write('WARNING: Skip non-biallelic site: %s\n'%('\t'.join(ss[:4])))
                    continue

                start = int(ss[1]) -1
                end = start + 1
                if end > len(refGenome[ss[0]]):
                    sys.stderr.write('WARNING: Skiped, POS exceed config size, config:%s, len: %d, call pos: %d\n'%(ss[0], len(refGenome[ss[0]]), end))
                    continue

                try:
                    #print(ss[0], start, end)
                    # sys.stderr.write(':::::::::: '+str(start)+'---'+str(end)+'\n')
                    ref_a = str(refGenome[ss[0]][start:end])
                    #print(ref_a)
                    ref = ss[3] #ref allele
                    alt = ss[4] #alt allele
                    if ref not in flipMap or alt not in flipMap:
                        sys.stderr.write('WARNING: (skiped) Allele coding error at: %s\n'%('\t'.join(ss[:5])))
                        continue

                    out = getOutputArray(ss, ref_a)
                    if not out:
                        #flip map
                        ss[3] = flipMap[ref]
                        ss[4] = flipMap[alt]
                        out = getOutputArray(ss, ref_a)
                        if not out: #failed after flipping strand.
                            sys.stderr.write('WARNING: failed even after flipping strand(skiped): %s\t%s\t%s (ref: %s)\n'%('\t'.join(ss[:3]), ref, alt, ref_a))
                            continue
                    sys.stdout.write('%s\n'%('\t'.join(out)))

                except KeyError as e:
                    sys.stderr.write('WARNING: Can not find contig [%s] in reference genome\n'%(ss[0]))
                    #sys.exit(-1)


            else:
                if line.startswith('#'):
                    sys.stdout.write('%s\n'%(line))
                if line.upper().startswith('#CHROM'):
                    data = True

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
