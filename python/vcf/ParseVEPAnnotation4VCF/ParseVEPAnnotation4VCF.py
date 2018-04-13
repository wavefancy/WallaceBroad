#!/usr/bin/env python3

"""

    Parse VEP annotation for VCF file.

    @Author: wavefancy@gmail.com

    Usage:
        ParseVEPAnnotation4VCF.py
        ParseVEPAnnotation4VCF.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output results to stdout.
        2. Parse the 'CSQ' field, make each transcript one line,
           Keeping the first 5 meta columns for each variants.

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

    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    num_meta = 5 #how many meta columns will keep for each variant.
    missing = 'NA'
    header = []
    indata = False
    for line in sys.stdin:
        line = line.strip()
        if line:
            if indata:  #Parse each variant.
                ss = line.split()
                out = ss[:num_meta]
                data = ss[7].split('CSQ=')[1].split(';')[0].split(',')
                for d in data:
                    dout = out + d.split('|')
                    dout = [ missing if not d else d for d in dout]
                    sys.stdout.write('%s\n'%('\t'.join(dout)))

            elif (not header and line.startswith('##INFO=<ID=CSQ')):
                header = line.split('Format:')[1][:-2].split('|')
            elif (line.startswith('#CHROM')):
                header = line.split()[:num_meta] + header
                sys.stdout.write('%s\n'%('\t'.join(header)))
                indata = True

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
