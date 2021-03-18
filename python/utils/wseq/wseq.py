#!/usr/bin/env python3

"""

    Enhanced version of GNU seq, which supports output ranges.
    @Author: wavefancy@gmail.com

    Usage:
        wseq.py -b int -e int -s int [-r]
        wseq.py -h | --help | -v | --version | -f | --format

    Notes:

    Options:
        -b int        The begin number of the sequence.
        -e int        The end number of the sequence.
        -s int        The step for the generator.
        -r            Generate the range list, both ends inclusive.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def ShowFormat():
    '''File format example'''
    print('''
# python3 wseq.py -b 1 -e 10 -s 4 -r
------------------------
1-4
5-8
9-10

python3 wseq.py -b 1 -e 10 -s 5
------------------------
1
6
''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    begin  = int(args['-b'])
    end    = int(args['-e'])  
    step   = int(args['-s'])
    grange = True if args['-r'] else False 

    # end +1 to shift the end as inclusive.
    for x in range(begin, end+1, step):
        if grange:
            t_end = x+(step-1)
            t_end = t_end if t_end <= end else end
            sys.stdout.write('%d-%d\n'%(x, t_end))
        else:
            sys.stdout.write('%d\n'%(x))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
