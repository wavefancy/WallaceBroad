#!/usr/bin/env python3

'''

    WColumnSelector: select records according to specific values in column.
    - updated version with switch flag.

    @Author: wavefancy@gmail.com, Wallace Wang.

    Usage:
        WColumnSelector.py (-t text | -c int) (-k|-r) -v text [--cp]
        WColumnSelector.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.

    Options:
        -c int        Column index for comparing, 1 based.
        -t txt        Specify column by column name, treat the first non-comment line as column name.
                      In this model, the title will be directly copy to stdout.
        -v txt        Value set for selection, values split by ','. eg. txt1|txt1,txt2.
        -k            Keep records if the value in '-v' value set.
        -r            Remove records if the value in '-v' value set.
        --cp          Directly copy comment line to stdout, no checking. Starts with '#'
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
#Input file format(stdin), first two columns as id pair, ignore other columns.
------------------------
#x      y
1       2
3       4

cat test.txt | python3 WColumnSelector.py -c 2 -k -v y,2
------------------------
#x      y
1       2

cat test.txt | python3 WColumnSelector.py -c 2 -r -v y,2
------------------------
3       4

cat test.txt | python3 WColumnSelector.py -t y -k -v 2
------------------------
#x      y
1       2

cat test.txt | python3 WColumnSelector.py -c 2 -k -v 4 --cp
------------------------
#x      y
3       4
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    COL = int(args['-c'])-1 if args['-c'] else -1 #Column for checking value.
    KEEPMODEL = False if args['-r'] else True
    COPYCOMENTS  = True if args['--cp'] else False
    KEYS = set([x for x in args['-v'].split(',')])
    INDEXMAP = dict()

    for line in sys.stdin:
        line = line.strip()
        if line :
            if COPYCOMENTS and line.startswith('#'):
                sys.stdout.write('%s\n'%(line))
                continue

            # Find column in title model.
            if (not INDEXMAP) and args['-t']:
                ss = line.split()
                for k,v in zip(ss, range(len(ss))):
                    if k in INDEXMAP:
                        sys.stderr.write('ERROR, Dupliciate values in title, -t model failed! DUP KEY: %s\n'%(k))
                        sys.exit(-1)
                    else:
                        INDEXMAP[k] = v
                if args['-t'] not in INDEXMAP:
                    sys.stderr.write('ERROR, Can not find key in title, please check!\n')
                    sys.exit(-1)
                else:
                    COL = INDEXMAP[args['-t']]
                #copy title line
                sys.stdout.write('%s\n'%(line))
                continue

            ss = line.split(None,COL+1)

            if KEEPMODEL: #keep
                if ss[COL] in KEYS:
                    sys.stdout.write('%s\n'%(line))
            else:
                if ss[COL] not in KEYS:
                    sys.stdout.write('%s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
