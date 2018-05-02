#!/usr/bin/env python3

"""

    Reset dnNSFP damaging annotion.

    @Author: wavefancy@gmail.com

    Usage:
        ResetDbNSFPDamaging.py
        ResetDbNSFPDamaging.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. If any transcript annotion has D or P, set as D.
            'D&N&D' -> D
            'P&P&P' -> D
        3. Only deal with filed with '&', keep all the others unchanged.

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

    def processRecord(d):
        '''Reset filed has "&", if any annotion is D set as D else set as N.
         if the input do not have '&', keep the orignal one.
        '''
        dd = d.upper().split('&')
        if len(dd) ==1:
            return d
        else:
            if 'D' in dd or 'P' in dd:
                return 'D'
            else:
                return 'N'

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            ss = [processRecord(x) for x in ss]
            sys.stdout.write('%s\n'%('\t'.join(ss)))
            
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
