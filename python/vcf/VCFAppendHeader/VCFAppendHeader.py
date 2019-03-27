#!/usr/bin/env python3

"""

    Append content to VCF header section.

    @Author: wavefancy@gmail.com

    Usage:
        VCFAppendHeader.py <headerlines>...
        VCFAppendHeader.py -h | --help | -v | --version | -f

    Notes:
        1. Read vcf file from stdin and output results to stdout.

    Options:
        <headerlines>...  One or more header lines to append to the header section.
                                The append lines is before of the #CHR line (sample list line).
        -h --help         Show this screen.
        -v --version      Show version.
        -f                Show format example.
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
        ''');
        sys.exit(0)

    H_lines =  args['<headerlines>']
    data = False
    for line in sys.stdin:
        if data:
            sys.stdout.write(line)

        else:
            if line[:6].upper().startswith('#CHROM'):
                for h in H_lines:
                    sys.stdout.write('%s\n'%(h))
                data = True
            sys.stdout.write(line)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
