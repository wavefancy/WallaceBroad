#!/usr/bin/env python3

"""

    Combine VCF files (in put as gz or flat text files).
    @Author: wavefancy@gmail.com

    Usage:
        CatVCFs.py <file.vcf.gz>...
        CatVCFs.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Concatenate multiple VCF files together, order as the appearence in parameters.
        2. Only keep the header from the first vcf.
        3. input vcf files either in ziped(.gz) or flat txt model.

    Options:
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
import codecs
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'UTF-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def ShowFormat():
    '''File format example'''
    print('''
    #VCF 01
    ------------------------
    # header1
    chr1 1

    #VCF 02
    ------------------------
    # hearder2
    chr2 2

    #Combined VCF
    ------------------------
    # header1
    chr1 1
    chr2 2
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    import gzip
    files = []
    for f in args['<file.vcf.gz>']:
        if f.endswith('.gz'):
            files.append(gzip.open(f, 'rt'))
        else:
            #files.append(open(f,'r'))
            files.append(open(f,'r',encoding="utf-8"))

    for line in files[0]:
        line = line.strip()
        if line:
            sys.stdout.write('%s\n'%(line))

    # sys.stdout.reconfigure(encoding='utf-8')
    for file in files[1:]:
        for line in file:
            line = line.strip()
            if line:
                if line[0] != '#':
                    sys.stdout.write('%s\n'%(line))

    #close files.
    [f.close() for f in files]

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
