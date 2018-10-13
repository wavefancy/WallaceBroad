#!/usr/bin/env python3

"""

    Add VCF Config information.
    @Author: wavefancy@gmail.com

    Usage:
        VCFAddContigInfo.py -r <ref.fai> [-c txt]
        VCFAddContigInfo.py -h | --help | -v | --version | -f

    Notes:
        1. Read vcf file from stdin and output results to stdout.

    Options:
        -r FILE       Fasta .fai file.
        -c txt        List the config name for adding, otherwise, loading all. e.g. 1,2|5.
        -h --help     Show this screen.
        -v --version  Show version.
        -f            Show format example.
    Dependency:
        docopt
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
zcat data/gene.vcf.gz | python3 /medpop/esp2/wallace/tools/python/VCFAddContigInfo.py -r /medpop/esp2/wallace/data/1kg/1kgref_hg19/human_g1k_v37.fasta.fai -c 1,2
              ''');
        sys.exit(0)

    refFile = args['-r']
    config_map = {}
    with open(refFile,'r') as infile:
        for line in infile:
            ss = line.split()
            config_map[ss[0]] = ss[1]

    chr_set = args['-c'].split(',') if args['-c'] else []
    data = False
    for line in sys.stdin:
        if data:
            sys.stdout.write(line)

        else:
            if line[:6].upper().startswith('#CHROM'):
                if chr_set:
                    for x in chr_set:
                        try:
                            sys.stdout.write('##contig=<ID=%s,length=%s>\n'%(x,config_map[x]))
                        except Exception as e:
                            sys.stderr.write('ERROR! Can not find contig name "%s" in fai file!\n'%(x))
                            sys.exit(-1)
                else:
                    for k,v in config_map.items():
                        sys.stdout.write('##contig=<ID=%s,length=%s>\n'%(k,v))
                data = True
            sys.stdout.write(line)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
