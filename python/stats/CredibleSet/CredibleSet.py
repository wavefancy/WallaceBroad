#!/usr/bin/env python3

"""

    Select the variants in a credible set base on specified threshold.
        *** Input should be ranked by 'PIP' from large to small. 
        *** This script will select the miminal number of variants,
        *** with total of these varints' 'PIP' >= specified_threshold.

    @Author: wavefancy@gmail.com

    Usage:
        CredibleSet.py -c txt -t float
        CredibleSet.py -h | --help | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout.
            *** Input should be ranked by PIP (-c column) numerically.
        2. Treat the first line as title.

    Options:
        -c txt     Column name for PIP, input should be ranked by this column.
        -t float   Threshold for the credible set.
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
# INPUT
# ------------
 PIP SNP
 0.4 A
 0.3 B
 0.2 C
 0.1 D
                                                                                                                                                                          
# cat in.txt | python3 ./CredibleSet.py -c PIP -t 0.8
# ------------
PIP SNP
0.4 A
0.3 B
0.2 C                       
    ''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    T_KEYS     = args['-c']
    WITH_TITLE = True
    THRESHOLD  = float(args['-t'])
    COL = -1

    INDEXMAP = {}
    CURRENT_TOTAL_PIP = 0.0
    for line in sys.stdin:
        line = line.strip()
        if line:
            if WITH_TITLE:
                if T_KEYS:
                    ss = line.split()
                    for k,v in zip(ss, range(len(ss))):
                        if k in INDEXMAP:
                            sys.stderr.write('ERROR, Dupliciate values in title, -t model failed! DUP KEY: %s\n'%(k))
                            sys.exit(-1)
                        else:
                            INDEXMAP[k] = v
                    COL = INDEXMAP[T_KEYS]

                sys.stdout.write('%s\n'%(line))
                WITH_TITLE = False

            else:
                ss = line.split()
                CURRENT_TOTAL_PIP += float(ss[COL])
                sys.stdout.write('%s\n'%(line))
                if CURRENT_TOTAL_PIP >= THRESHOLD:
                    break
                
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
