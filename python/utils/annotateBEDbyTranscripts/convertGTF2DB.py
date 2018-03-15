#!/usr/bin/env python3

"""

    Convert GTF file to sqlite DB format for easy load by gffutils

    @Author: wavefancy@gmail.com

    Usage:
        convertGTF2DB.py -o file -i file
        convertGTF2DB.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read input bed from stdin, and output results to stdout.

    Options:
        -o file       GFF gene annotatioin file.
        -i file       Input GFF annotatioin file.
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
    # print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    # The load inpu should be like the gencode gtf file.
    # The file should already have genes and transcripts on separate lines.
    # This means we can avoid the gene and transcript inference, which saves time.
    # merge_strategy='merge', use this to solve duplicate id issues.
    import gffutils
    db = gffutils.create_db(args['-i'],
    args['-o'],
    keep_order=True,
    merge_strategy="create_unique",
    sort_attribute_values=True,
    disable_infer_genes=True, disable_infer_transcripts=True)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
