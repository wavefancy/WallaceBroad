#!/usr/bin/env python3

"""

    Read format arguments from stdin and output pattern guided output to stdout.
    @Author: wavefancy@gmail.com

    Usage:
        wprintf.py <pattern> [-c] [-s] [-l]
        wprintf.py -h | --help | -v | --version | -f | --format

    Notes:

    Options:
        -d pattern    The string pattern for format output.
        -c            Collapse the output as a single line.
        -l            In line mode, do not split at each input line.
                        In this mode, we can only have one place holder,
                        as we only have one argument.
        -s            Set the place holder as [], instead of {}.
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
# INPUT test.txt file.
------------------------
1 2 3
K L M

cat test.txt | python3 ./wprintf.py 'A{} B{} C{}' -c
------------------------
A1 B2 C3 AK BL CM

cat test.txt | python3 ./wprintf.py 'A{} B{} C{}'
cat test.txt | python3 ./wprintf.py 'A[] B[] C[]' -s
------------------------
A1 B2 C3
AK BL CM

cat test.txt | python3 ./wprintf.py 'linemode {}' -l
------------------------
linemode 1 2 3
linemode K L M
''')

if __name__ == '__main__':
    args = docopt(__doc__, version='3.0')

    singleline = True if args['-c'] else False
    linemode   = True if args['-l'] else False

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    stingpattern = args['<pattern>']
    if(args['-s']):
        stingpattern = stingpattern.replace('[','{').replace(']','}')

    out_array = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            if linemode:
                out = stingpattern.format(line)
            else:
                ss = line.split()
                out = stingpattern.format(*ss)

            # api: https://www.geeksforgeeks.org/python-format-function/
            # *ss for fitting a array list.
            
            if singleline:
                out_array.append(out)
            else:
                sys.stdout.write('%s\n'%(out))

    if singleline:
        sys.stdout.write('%s\n'%(' '.join(out_array)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
