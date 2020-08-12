#!/usr/bin/env python3

"""

    Parse the annotaion format the key-value pair are connected by equal sign('=').
    For example: ID=ENST00000456328.2;Parent=ENSG00000223972.5;gene_id=ENSG00000223972.5_2.
    Convert the this compact format to a tsv table format.

    @Author: wavefancy@gmail.com

    Usage:
        EqualAnnoParser.py  -c int -k txts [-m] [--cs txt]
        EqualAnnoParser.py -h | --help | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout.

    Options:
        -c int     Column index for the key-value pairs.
        -k txts    Key list to extract for the output, eg. ID|ID,gene_id   
        -m         Directly copy comment lines, startswith '--cs'.
        --cs txt   Set the start characters for comment line, [#]. 
        -h --help  Show this screen.
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
#INPUT:
----------------
ID=ENSG00000223972.5;gene_id=ENSG00000223972.5_2;gene_name=DDX11L1

#OUTPUT: -c 1 -k 'ID,gene_id'
----------------
ID=ENSG00000223972.5;gene_id=ENSG00000223972.5_2;gene_name=DDX11L1   ENSG00000223972.5       ENSG00000223972.5_2
''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    COMMENTS_START = args['--cs'] if args['--cs'] else '#'
    COPY_COMMENTS  = True if args['-m'] else False
    KEYS           = args['-k'].split(',')
    KEYSET         = set(KEYS)
    COLINDEX       = int(args['-c']) -1
    maxSplit       =  COLINDEX + 1

    for line in sys.stdin:
        line = line.strip()
        if line:
            if COPY_COMMENTS and line.startswith(COMMENTS_START):
                sys.stdout.write('%s\n'%(line))
                continue

            else:
                ss = line.split(None, maxSplit)
                # print(ss)
                kv_map = {}
                kvs = ss[COLINDEX].split(';')
                for x in kvs:
                    if x:
                        kv = x.split('=')
                        if kv[0] in KEYSET:
                            kv_map[kv[0]] = kv[1]
                        if len(kv_map) == len(KEYS):
                            break

                for k in KEYS:
                    ss.append(kv_map[k])

                sys.stdout.write('%s\n'%('\t'.join(ss)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
