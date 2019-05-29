#!/usr/bin/env python3

"""

    Replace content according to key map values.

    @Author: wavefancy@gmail.com

    Usage:
        KeyMapReplace.py -p <key-value-pair-file> -k <kcol> (-r <rcol>[,default] | -a aValue) [-d delimter] [-x] [-w] [-c] [--cs txt]
        KeyMapReplace.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and replace content based on key-map values.
        2. Output results to stdout.

    Options:
        -p <key-map-pair-file>  Key value pairs, one entry one line.
                                [1,n] columns as key, n is the number of keys '-k'.
        -k <kcol>               Colums as key in stdin, column index starts from 1, eg 1|1,3
        -r <rcol>[,default]     Colum to replace in stdin, column index starts from 1.
                                  if in '-r <rcol>' mode, change the matched records, keep other untouched.
                                  if in <rcol>[,default] mode, change the matched, replace the unmatched as the 'default' value.
                                     this will erase the '-x' effects, output all records.
        -a aValue               Add one column at line end, other than replace one column,
                                  add 'aValue' if no key matching.
        -d delimter             Delimiter to split columns from stdin.
        -x                      Close output for unmatched records, default output.
        -w                      Warning out unmatched records to stderr.
        -c                      Directly copy comment lines to stdout.
        --cs txt                Set the starting text for comment lines, default #.
        -h --help               Show this screen.
        -v --version            Show version.
        -f --format             Show input/output file format example.

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

# cat in.txt | python3 KeyMapReplacer.py -p kv_map.txt -k 1 -r 2,DEFAULT
------------------------
Warning: Duplicate keys, only keep first entry. Skip: 2   c   10
Warning: Duplicate keys, only keep first entry. Skip: 2   a   10
1       DEFAULT 3
2       K       10      4
3       DEFAULT 5
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='4.0')
    #version 3.0
    # 1. Add function to support multiple columns as key.
    #    Treat all the columns except the last one in the key-map-pair-file as key.
    #    Columns for key were concatentated by '-'

    #version 4.0
    # 1. add option to split kep colum from stdin.

    # print(args)
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

    keep_unmatch = False if args['-x'] else True
    warn_unmatch = True  if args['-w'] else False

    COMMENT_STRING = args['--cs'] if args['--cs'] else '#'
    COPY_COMMENTS = True if args['-c'] else False

    #read key-value pairs
    kv_map = {}
    n_content = ''
    for line in open(args['-p'],'r'):
        line = line.strip()
        if line:
            ss = line.split()
            k = '-'.join(ss[0:len(kcols)])
            if k not in kv_map:
                kv_map[k] = ss[len(kcols):]

                if not n_content:
                    n_content = len(kv_map[k])
            else:
                sys.stderr.write('Warning: Duplicate keys, only keep first entry. Skip: %s\n'%(line))

    # Replace one colum.
    if args['-r']:
        pp = args['-r'].split(',')
        rcol = int(pp[0]) -1
        Change_Unmatched = True if len(pp) == 2 else False
        if Change_Unmatched:
            keep_unmatch = True

        for line in sys.stdin:
            line = line.strip()
            if line:
                # copy comment lines.
                if COPY_COMMENTS and line.startswith(COMMENT_STRING):
                    sys.stdout.write('%s\n'%(line))
                    continue

                ss = line.split(delimiter)

                k = '-'.join([ss[x] for x in kcols])
                if k in kv_map:
                    ss[rcol] = '\t'.join(kv_map[k])
                    sys.stdout.write('%s\n'%('\t'.join(ss)))
                else:
                    if keep_unmatch:
                        if Change_Unmatched:
                            ss[rcol] = pp[1]
                            sys.stdout.write('%s\n'%('\t'.join(ss)))
                        else:
                            sys.stdout.write('%s\n'%('\t'.join(ss)))

                    if warn_unmatch:
                        sys.stderr.write('W_NOMATCH: %s\n'%('\t'.join(ss)))

    # add one more colum.
    if args['-a']:
        val = [args['-a'] for x in range(n_content)]
        for line in sys.stdin:
            line = line.strip()
            if line:
                # copy comments line.
                if COPY_COMMENTS and line.startswith(COMMENT_STRING):
                    sys.stdout.write('%s\n'%(line))
                    continue

                ss = line.split(delimiter)

                k = '-'.join([ss[x] for x in kcols])
                if k in kv_map:
                    sys.stdout.write('%s\t%s\n'%('\t'.join(ss), '\t'.join(kv_map[k])))
                else:
                    if keep_unmatch:
                        sys.stdout.write('%s\t%s\n'%('\t'.join(ss), '\t'.join(val)))
                    if warn_unmatch:
                        sys.stderr.write('W_NOMATCH: %s\t%s\n'%('\t'.join(ss), '\t'.join(val)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
