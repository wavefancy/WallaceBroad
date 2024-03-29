#!/usr/bin/env python3

'''

    Add title for the input stream, and output to stdout.

    @Author: wavefancy@gmail.com, Wallace Wang.

    Usage:
        AddTitle.py [-d delimiter] [-s delimiter] <title>...
        AddTitle.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.

    Options:
        -d delimiter  Set output title delimiter, default tab.
        -s delimiter  Split each title element by 'delimiter', 
                        and add as new title elements.
        -h --help     Show this screen.
        --version     Show version.
        -f --format   Show input/output file format example.

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.
from docopt import docopt

def ShowFormat():
    '''File format example'''
    print('''
#echo 'A B C' | python3 AddTitle.py -d ' ' 1 2 3
------------------------
1 2 3
A B C
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    DELIMITER = args['-d'] if args['-d'] else '\t'
    TTs = []
    if args['-s']:
        for x in args['<title>']:
            TTs += x.split(args['-s'])
    else:
        TTs = args['<title>']

    sys.stdout.write('%s\n'%(DELIMITER.join(TTs)))
    for line in sys.stdin:
        sys.stdout.write(line)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
