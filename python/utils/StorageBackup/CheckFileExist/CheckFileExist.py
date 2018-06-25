#!/usr/bin/env python

"""

    Check whether the file existing or not.

    @Author: wavefancy@gmail.com

    Usage:
        CheckFileExist.py [--gz]
        CheckFileExist.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin (file name line by line), and output results to stdout.

    Options:
        --gz          Test whether a missing file has .gz format file.
                          IF yes, output the file with .gz
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
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    GZ_END   = '.gz'
    CHECK_GZ = True if args['--gz'] else False # checking gzipped files.

    for line in sys.stdin:
        line = line.strip()
        if line:

            if path.isfile(line):
                sys.stdout.write('%s\n'%(line))

            else:
                if CHECK_GZ:
                    line_gz = line + GZ_END
                    if path.isfile(line_gz):
                        sys.stdout.write('%s\n'%(line_gz))
                        continue

                sys.stderr.write('MISSING_file: %s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
