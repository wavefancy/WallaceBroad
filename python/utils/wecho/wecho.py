#!/usr/bin/env python3

"""

    Copy input multiline string to stdout, with the ability to filter comments.
    @Author: wavefancy@gmail.com

    Usage:
        wecho.py <string> [-d commendDelimeter] [-l linecomment] [-b linebreaker]
        wecho.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Copy input string argument to stdout.
        2. Remove newline character, combine mutilines to a single line.
        3. Remove comments from input string, comments was surrounded by %, see example by -f.
            Single line comment can be started by linecomment characters, default #.


    Options:
        -d string     Replace default pair comment delimter(%%) as 'string'.
        -l string     String for declearing a linecomment, default '#' or '//'.
        -b string     String for linebreaker, start a new line after these characters, default !.
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
    #Input example
    ------------------------
    "
    123 %% comments %%
    456 %% multiple %%
    line
    # comments
    # line comments
    789
    !new line
    123 %% comments%% 456 789"

    #Output example
    ------------------------
    123  456 789
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='3.0')
    #version 2.0
    #1. add function for line comments.

    commentDelimeter = '%%'
    # linecomment = '//'
    linecomment = '#'
    linebreaker = '!'

    if args['-d']:
        commentDelimeter = args['-d']
    if args['-l']:
        linecomment = args['-l']
    if args['-b']:
        linebreaker = args['-b']
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    #split by lines.
    import re
    lines = args['<string>'].strip()
    lines = lines.split(commentDelimeter)
    if len(lines) %2 == 0:
        sys.stderr.write('Error: Comment delimter should be appeared in pair!.\n')
        sys.exit(-1)

    #skip comments
    arr2 = []
    for i in range(0,len(lines),2):
        arr2.append(lines[i])

    #remove line breakers.
    arr1 = []
    for x in arr2:
        if x:
            for y in x.splitlines():
                y = y.strip()
                # y.startswith('//') make it compatible with old scripts.
                if not (y.startswith(linecomment) or y.startswith('//')): #skip line commented line.
                    arr1.append(y)

    out = ' '.join(arr1)
    out = re.sub(r'\s+',' ',out)
    out = out.split(linebreaker)
    for x in out:
        x = x.strip()
        sys.stdout.write('%s\n'%(x))

    # if len(lines) == 1:
    #     lines = re.split('\\\\n',lines[0])

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
