#!/usr/bin/env python3

"""

    Replace content according to key map values.

    @Author: wavefancy@gmail.com

    Usage:
        KeyMapReplace.py -p <key-value-pair-file> -k <kcol> (-r <rcol> | -a aValue) [-d delimter]
        KeyMapReplace.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and replace content based on key-map values.
        2. Output results to stdout.

    Options:
        -p <key-map-pair-file>  Key value pairs, one entry one line.
                                [1,n] columns as key, n is the number of keys '-k'.
        -k <kcol>     Colums as key in stdin, column index starts from 1, eg 1|1,3
        -r <rcol>     Colum to replace in stdin, column index starts from 1.
        -a aValue     Add one column at line end, other than replace one column,
                        add 'aValue' if no key matching.
        -d delimter   Delimiter to split columns from stdin.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def ShowFormat():
    '''File format example'''
    print('''
    #kv_map:
    ------------------------
2   K
2   c
2   a

    #input:
    ------------------------
1   a
2   c
3   d

    #output: -p kv_map -k 1 -r 2
    ------------------------
1       a
2       K
3       d

    #output: -p kv_map -k 1 -a aval
    ------------------------
1       a       aval
2       c       K
3       d       aval
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='4.0')
    #version 3.0
    # 1. Add function to support multiple columns as key.
    #    Treat all the columns except the last one in the key-map-pair-file as key.
    #    Columns for key were concatentated by '-'

    #version 4.0
    # 1. add option to split kep colum from stdin.

    #print(args)
    #sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)
    if args['-a'] and args['-r']:
        sys.stderr.write('ERROR: option -a|-r can only be applied by one of them.\n')
        sys.exit(-1)
    delimiter = None
    if args['-d']:
        delimiter = args['-d']

    #Replace one colum
    kcols = [int(x) -1 for x in args['-k'].split(',')]

    #read key-value pairs
    kv_map = {}
    for line in open(args['-p'],'r'):
        line = line.strip()
        if line:
            ss = line.split()
            k = '-'.join(ss[0:len(kcols)])
            if k not in kv_map:
                kv_map[k] = ss[len(kcols):]
            else:
                sys.stderr.write('Warning: Duplicate keys, only keep first entry. Skip: %s\n'%(line))


    if args['-r']:
        rcol = int(args['-r']) -1
        for line in sys.stdin:
            line = line.strip()
            if line:
                ss = line.split(delimiter)

                k = '-'.join([ss[x] for x in kcols])
                if k in kv_map:
                    ss[rcol] = kv_map[k]
                sys.stdout.write('%s\n'%('\t'.join(ss)))

    if args['-a']:
        val = args['-a']
        for line in sys.stdin:
            line = line.strip()
            if line:
                ss = line.split(delimiter)

                k = '-'.join([ss[x] for x in kcols])
                if k in kv_map:
                    sys.stdout.write('%s\t%s\n'%('\t'.join(ss), '\t'.join(kv_map[k])))
                else:
                    sys.stdout.write('%s\t%s\n'%('\t'.join(ss), val))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
