#!/usr/bin/env python3

"""

    Subset iput by keys.

    @Author: wavefancy@gmail.com

    Usage:
        SubsetByKey.py (-f keyfile | -v vals) (-k|-r) (-c ints | -t txts) [--title] [-m] [-d txt]
        SubsetByKey.py -h | --help | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout.
        2. Output results from stdout.

    Options:
        -f keyfile    Input key list files.
        -v vals       Key values, e.g.: txt1,txt2 | txt3.
        -t txts       Value set for column selection, values split by ','. eg. txt1|txt1,txt2.
                      The first line will treat as title.
        -k            Keep key indicated records.
        -r            Remove key indicated records.
        -c ints       Column index for comparing with keys, eg. 1|1,2. 1 based.
        -m            Directly copy comment lines, startswith '#'.
        -d txt        Column delimiter, default white-spaces. tab for '\\t'.
        --title       Indicate first non-comment line as title, no filterring.
        -h --help     Show this screen.
        --version  Show version.
        --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.
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
    WITH_TITLE     = True if args['--title'] else False
    COPY_COMMENTS  = True if args['-m'] else False
    KEYS           = [int(x)-1 for x in args['-c'].split(',')] if args['-c'] else []
    DELIMITER      = args['-d'] if args['-d'] else None
    if DELIMITER and DELIMITER.lower() == 'tab':
        DELIMITER = '\t'
    # Select by title keys.
    T_KEYS = set([x for x in args['-t'].split(',')]) if args['-t'] else None
    if T_KEYS:
        WITH_TITLE = True

    #read key sets.
    my_keys = set()
    if args['-v']:
        my_keys = set(args['-v'].split(','))
    else:
        with open(KEY_FILE,'r', encoding="utf-8") as kf:
            for line in kf:
                line = line.strip()
                if line:
                    my_keys.add('-'.join(line.split(DELIMITER)))

    if KEYS:
        maxSplit = max(KEYS) + 2
    INDEXMAP = {}
    for line in sys.stdin:
        line = line.strip()
        if line:
            if COPY_COMMENTS and line.startswith('#'):
                sys.stdout.write('%s\n'%(line))
                continue

            if WITH_TITLE:
                if T_KEYS:
                    ss = line.split()
                    for k,v in zip(ss, range(len(ss))):
                        if k in INDEXMAP:
                            sys.stderr.write('ERROR, Dupliciate values in title, -t model failed! DUP KEY: %s\n'%(k))
                            sys.exit(-1)
                        else:
                            INDEXMAP[k] = v
                    for k in T_KEYS:
                        if k not in INDEXMAP:
                            sys.stderr.write('ERROR, key not in title: %s\n'%(k))
                            sys.exit(-1)
                        else:
                            KEYS.append(INDEXMAP[k])
                    maxSplit = max(KEYS) + 2

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
