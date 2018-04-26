#!/usr/bin/env python3

"""

    Convert Transvar AA change to gnomic change output to table format.

    @Author: wavefancy@gmail.com

    Usage:
        TransvarP2G.py [--vep]
        TransvarP2G.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        3. See example by -f.

    Options:
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    #input:
    ------------------------
input   transcript      gene    strand  coordinates(gDNA/cDNA/protein)  region  info
ANGPTL3:p.F295L CCDS622 (protein_coding)        ANGPTL3 +       chr1:g.63068003T>C/c.883T>C/p.F295L     inside_[cds_in_exon_5]      CSQN=Missense;reference_codon=TTC;candidate_co
dons=CTT,CTG,CTA,CTC,TTA,TTG;candidate_snv_variants=chr1:g.63068005C>A,chr1:g.63068005C>G;candidate_mnv_variants=chr1:g.63068003_63068005delTTCinsCTT,chr1:g.63068003_63068005delT
TCinsCTG,chr1:g.63068003_63068005delTTCinsCTA;source=CCDS
ANGPTL3:p.L53W  CCDS622 (protein_coding)        ANGPTL3 +       chr1:g.63063395T>G/c.158T>G/p.L53W      inside_[cds_in_exon_1]  CSQN=Missense;reference_codon=TTG;candidate_codons
=TGG;source=CCDS

    #output:
    ------------------------
p.F295L chr1    63068003        T       C
p.F295L chr1    63068005        C       A
p.F295L chr1    63068005        C       G
p.L53W  chr1    63063395        T       G
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    def convertG(g):
        '''reformat gnomic change format'''
        ss = g.split(':g.')
        out = [ss[0]]
        out.append(ss[1][:-3])
        out.append(ss[1][-3])
        out.append(ss[1][-1])
        return '\t'.join(out)

    title = True
    for line in sys.stdin:
        line = line.strip()
        if line:
            if title:
                title = False
                continue
            ss = line.split()
            coor1 = ss[5].split('/')
            # out = []
            # out.append(coor1[-1])

            candiates = ''
            temp = ss[7].split(';')
            for x in temp:
                if x.startswith('candidate_snv_variants'):
                    candiates = x.split('candidate_snv_variants=')[1];
                    break

            gg = [coor1[0]]
            if candiates:
                gg = gg + candiates.split(',')

            if args['--vep']:
                for g in gg:
                    sys.stdout.write('%s\n'%(g))
            else:
                for g in gg:
                    sys.stdout.write('%s\t%s\n'%(coor1[-1], convertG(g)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
