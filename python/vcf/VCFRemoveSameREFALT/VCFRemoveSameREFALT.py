#!/usr/bin/env python3

"""

    Remove a vcf line if the REF and ALt allele is the same.

    @Author: wavefancy@gmail.com

    Usage:
        VCFRemoveSameREFALT.py
        VCFRemoveSameREFALT.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, output to stdout.
        3. Output results to stdout.

    Options:
        -h --help       Show this screen.
        -v --version    Show version.
        -f --format     Show format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    input vcf example(abstracted):
----------------------
chr2    13649   .  G       C

    out vcf example:
----------------------
chr2    13649   chr2:13649:G:C  G       C
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    output = False
    for line in sys.stdin:
        line = line.strip()
        if line:
            if output:
                #output results.
                ss = line.split(None, maxsplit=7)
                if ss[3] != ss[4]:
                    sys.stdout.write('%s\n'%('\t'.join(ss)))

            else:
                if line.startswith('##'):
                    sys.stdout.write('%s\n'%(line))
                elif line.startswith('#C') or line.startswith('#c'):
                    output = True
                    sys.stdout.write('%s\n'%(line))

sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
