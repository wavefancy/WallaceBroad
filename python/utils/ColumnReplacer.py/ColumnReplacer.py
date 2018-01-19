#!/usr/bin/env python3

'''
    ColumnReplacer

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Algorithms
    1. Replace column value by key-value pairs.

    @Version2.0
    1. Add function to directly copy comments line to stdout.

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def help():
    sys.stderr.write('''
    -------------------------------------
    ColumnReplacer
    -------------------------------------

    @Author: wavefancy@gmail.com
    @Version: 2.0

    @Usages:
    para1: Column index, which column want to be replaced.
    para2: key=value pairs. eg. af=12,12=34

    @Optional:
    -c : Directly copy comments line to stdout, no action performed, comments started by #.

    @Notes:
    1. Read input from stdin, and output to stdout.
    2. Every entry only apply rule once, so af=12,12=34, after 'af' be replaced by '12',
        '12' will not be replaced by '34' again at this row.
    3. af=12,12=34,*=ef: '*' represents all other values. All the other values other than 'af','12'
        will be replaced as 'ef'.
        If '*' wasn't set, only replace exact match.
    4. Column index starts from 1.
    -------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)

if __name__ == '__main__':
    args = []
    copyComments = False
    for x in sys.argv:
        if x == '-c':
            copyComments = True
        else:
            args.append(x)

    sys.argv = args
    if len(sys.argv) != 3:
        help()

    col_index = int(sys.argv[1]) -1
    other = False # * stands all other values.
    o_value = ''
    ss = sys.argv[2].strip().split(',')
    key_map = {}
    for x in ss:
        xx = x.split('=')
        if xx[0] == '*':
            other = True
            o_value = xx[1]
        else:
            key_map[xx[0]] = xx[1]

    for line in sys.stdin:
        line = line.strip()
        if line :
            if copyComments and line.startswith('#'):
                sys.stdout.write('%s\n'%(line))
                continue

            ss = line.split(None,col_index+1)

            if ss[col_index] in key_map:
                ss[col_index] = key_map[ ss[col_index] ]
            else:
                if other:
                    ss[col_index] = o_value

            sys.stdout.write('%s\n'%('\t'.join(ss)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
