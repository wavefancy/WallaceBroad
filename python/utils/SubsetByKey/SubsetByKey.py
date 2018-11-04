#!/usr/bin/env python3

"""

    Subset iput by keys.

    @Author: wavefancy@gmail.com

    Usage:
        SubsetByKey.py -f keyfile (-k|-r) -c ints [-t] [-m] [-d txt]
        SubsetByKey.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout.
        2. Output results from stdout.

    Options:
        -f keyfile    Input key list files.
        -k            Keep key indicated records.
        -r            Remove key indicated records.
        -c ints       Column index for comparing with keys, eg. 1|1,2. 1 based.
        -t            Indicate first non-comment line as title, no filterring.
        -m            Directly copy comment lines, startswith '#'.
        -d txt        Column delimiter, default white-spaces. tab for '\\t'.
        -h --help     Show this screen.
        -v --version  Show version.
        --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

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

    KEY_FILE       = args['-f']
    KEEP           = True if args['-k'] else False
    WITH_TITLE     = True if args['-t'] else False
    COPY_COMMENTS  = True if args['-m'] else False
    KEYS           = [int(x)-1 for x in args['-c'].split(',')]
    DELIMITER      = args['-d'] if args['-d'] else None
    if DELIMITER and DELIMITER.lower() == 'tab':
        DELIMITER = '\t'

    #read key sets.
    my_keys = set()
    with open(KEY_FILE,'r', encoding="utf-8") as kf:
        for line in kf:
            line = line.strip()
            if line:
                my_keys.add('-'.join(line.split(DELIMITER)))

    maxSplit = max(KEYS) + 2
    for line in sys.stdin:
        line = line.strip()
        if line:
            if COPY_COMMENTS and line.startswith('#'):
                sys.stdout.write('%s\n'%(line))
                continue

            if WITH_TITLE:
                sys.stdout.write('%s\n'%(line))
                WITH_TITLE = False
            else:
                ss = line.split(DELIMITER, maxSplit)
                ikeys = '-'.join([ss[x] for x in KEYS])

                if KEEP:
                    if ikeys in my_keys:
                        sys.stdout.write('%s\n'%(line))
                else:
                    if ikeys not in my_keys:
                        sys.stdout.write('%s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
