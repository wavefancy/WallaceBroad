#!/usr/bin/env python3

"""

    Check file compress status.
    If the compress process was interrupted, both the original and the original.gz will be existing.

    @Author: wavefancy@gmail.com

    Usage:
        CheckCompress.py
        CheckCompress.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin (file name line by line), and output results to stdout.
        2. Only output files with compressing interrupted.

    Options:
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)
import os.path as path

def ShowFormat():
    '''Input File format example:'''
    print('''
#-----INPUT------
test.txt
test2.txt

#-----OUTPUT-----
test2.txt
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    for line in sys.stdin:
        line = line.strip()
        if line:
            com_file = line + '.gz'
            if path.isfile(line) and path.isfile(com_file):
                sys.stdout.write('%s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
