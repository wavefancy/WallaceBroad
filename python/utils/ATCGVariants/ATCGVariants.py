#!/usr/bin/env python3

"""

    Check whether a variant site is AT or GC. For it's hard to make strand consistent.
    @Author: wavefancy@gmail.com

    Usage:
        ATCGVariants.py -a int -b int [-c] [-r] [-m]
        ATCGVariants.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. ***Skip checking for indels, only for SNPs***
        3. See example by -f.

    Options:
        -a int        Column index for the first(ref) allele, index starts from 1.
        -b int        Column index for the second(alt) allele.
        -c            Skip comment checking line, comment line started by '#'
        -r            Remove AT, GC sites, while keep all the other content.
                      Otherwise output AT/GC sites, default.
        -m            Output comment line, default false.
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
    # -a 5 -b 6
    ------------------------
1       1:82154 0       82154   T       A
1       1:752566        0       752566  C       G
1       1:752721        0       752721  G       A

    #output:
    ------------------------
1       1:82154 0       82154   T       A
1       1:752566        0       752566  C       G
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    col1 = int(args['-a']) -1
    col2 = int(args['-b']) -1
    maxsplit = max(col1, col2) +1

    SkipComment = False
    if args['-c']:
        SkipComment = True
    RemoveATGC = False
    if args['-r']:
        RemoveATGC = True
        #SkipComment = False
    OutComment = False
    if args['-m']:
        OutComment = True

    AT=['A', 'T']
    CG=['C', 'G']
    for line in sys.stdin:
        line = line.strip()
        if line:
            skip = False
            if SkipComment and line.startswith('#'):
                skip = True
            if OutComment and line.startswith('#'):
                sys.stdout.write('%s\n'%(line))
                skip = True
            if skip:
                continue

            ss = line.split(None, maxsplit)
            alleles = []
            alleles.append(ss[col1].upper())
            alleles.append(ss[col2].upper())
            alleles = sorted(alleles)

            if RemoveATGC:
                if not(alleles == AT or alleles == CG):
                    sys.stdout.write('%s\n'%(line))
            else:
                if alleles == AT or alleles == CG:
                    sys.stdout.write('%s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
