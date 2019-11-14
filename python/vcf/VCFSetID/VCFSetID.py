#!/usr/bin/env python3

"""

    Set/Replace ID for VCF file. setID as : chr:pos:ref:alt

    @Author: wavefancy@gmail.com

    Usage:
        VCFSetID.py [-i] [-s]
        VCFSetID.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, setID as : chr:pos:ref:alt.
        3. Output results to stdout.

    Options:
        -i              Include old rsID.
        -s              Sort the ref and alt alleles, sorted([ref,alt])
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

    IncludeOld = False
    if args['-i']:
        IncludeOld = True

    # infile.close()
    output = False
    for line in sys.stdin:
        line = line.strip()
        if line:
            if output:
                #output results.
                ss = line.split(None, maxsplit=7)

                # check if need to sort ref, alt alleles.
                stemp = sorted(ss[3:5]) if args['-s'] else ss[3:5]

                if IncludeOld:
                    ss[2] = ss[0] + ':' + ss[1] + ':' + stemp[0] + ':' + stemp[1] + ':' + ss[2]
                else:
                    ss[2] = ss[0] + ':' + ss[1] + ':' + stemp[0] + ':' + stemp[1]
                sys.stdout.write('%s\n'%('\t'.join(ss)))
                #sys.stdout.write('%s\n'%('\t'.join([ss[x] for x in idIndex])))

            else:
                if line.startswith('##'):
                    sys.stdout.write('%s\n'%(line))
                elif line.startswith('#C') or line.startswith('#c'):
                    output = True
                    sys.stdout.write('%s\n'%(line))

sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
