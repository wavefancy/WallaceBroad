#!/usr/bin/env python3

"""

    A new enhanced implementation for cut.
    @Author: wavefancy@gmail.com

    Usage:
        wcut.py (-f string | --tf file | -t titles) [-d string] [-c] [-a string] [--cs txt]
        wcut.py -h | --help | -v | --version | --format

    Options:
        -f string  Specifiy the columns want to cut.(eg. -f4,3; -f4,2-1, -f5-2)
        -t titles  Open title mode, one or more titles. eg. -t title1,title2,title3
        -d string  Set the delimiter for fields. 'tab' for Tab.'\\t'
        --tf file  Read title columns from file. (eg. -tf filename).
                        columns separated by WHITESPACE.
        -c         Open copy mode, directly copy comment line to stdout, comments started by '#'.
        --cs txt   Set the comment start string as 'txt', default it's '#'.
        -a string  Set the default value as 'string' if column value is empty.

        -h --help     Show this screen.
        -v --version  Show version.
        --format   Show input/output file format example.

    Notes:
        1. (-f mode): Important, different with unix 'cut', the output columns' order
           is dependent on the occurance order in -f option, not the occurance in input file.
        2. (-t|-tf mode): If -t specified, the fist line were treated as title.
           output based on the occurance oder of input parameters.
        3. Both for the input and output, columns are seperated by whitespace('\\t').
        4. Read input from stdin, and output to stdout.
        5. Column index starts from 1.
"""

import sys
from docopt import docopt
import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def ShowFormat():
    sys.stderr.write('''
    -------------------------------------------
    Cut columns from stdin input
    -------------------------------------------
    -------------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)

class P(object):
    outArrayId = [] # output array id. index
    title = False
    tArray = [] # title parameters.
    delimiter = ''
    #toEnd = False #output all the column from a starting point.
    First = True
    copyComments = False

    maxSplitTime = 0
    isSplitFixed = False #whether split a fix number of times.
    aVal = '' #whether add value to empty fields.

def runApp():
    # print(P.delimiter)
    if P.title:
        line = sys.stdin.readline()
        if P.delimiter:
            ss = line.strip().split(P.delimiter)
        else:
            ss = line.strip().split()

        for x in P.tArray:
            try:
                ii = ss.index(x)
                P.outArrayId.append(ii)
            except ValueError:
                sys.stderr.write('In title,can\'t find: %s\nPlease check!\n'%(x))
                sys.exit(-1)
        #output title line
        s_out = [ss[i] for i in P.outArrayId]
        sys.stdout.write('\t'.join(s_out))
        sys.stdout.write('\n')

    def addValue(x):
        '''add a set value if x not True'''
        if x:
            return x
        else:
            return P.aVal

    COMMENTS = args['--cs'] if args['--cs'] else '#'
    for line in sys.stdin:
        line = line.strip('\n')
        if line:
            if P.copyComments:
                if line.startswith(COMMENTS):
                    sys.stdout.write('%s\n'%(line))
                    continue

            if not P.isSplitFixed:
                if P.delimiter:
                    ss = line.split(P.delimiter)
                else:
                    ss = line.split()
            else: #split fixed number of times, improve performance, since V6.0
                if P.delimiter:
                    ss = line.split(P.delimiter,P.maxSplitTime)
                else:
                    ss = line.split(None, P.maxSplitTime)

            if P.First: #expand negative values, negative values means output to the end column from a starting points.
                t_out = []
                for x in P.outArrayId:
                    if x >= 0:
                        t_out.append(x)
                    else:
                        [t_out.append(k) for k in range(t_out[-1]+1, len(ss))]
                P.outArrayId = t_out
                P.First = False

            if not P.isSplitFixed:
                P.maxSplitTime = max(P.outArrayId) +1
                P.isSplitFixed = True

            #output one line
            try:
                s_n = [ss[i] for i in P.outArrayId]
            except IndexError:
                sys.stderr.write('ERROR: array index error: %d\n'%(len(ss)))
                sys.stderr.write('Line content: %s\n'%(ss))
                sys.exit(-1)

            if P.aVal:
                s_n  = [addValue(x) for x in s_n]

            sys.stdout.write('\t'.join(s_n))
            sys.stdout.write('\n')

    sys.stdout.close()

if __name__ == '__main__':
    #check delimiter
    args = docopt(__doc__, version='7.0')
    # print(args)

    if args['-d']:
        P.delimiter = args['-d']
        if P.delimiter == 'tab':
            P.delimiter = '\t'

    if args['-c']:
        P.copyComments = True
    if args['--tf']:
        P.First = False # -t mode, do not need expand.
        P.title = True

        for line in open(args['--tf']): # read title lines from file
            line = line.strip()
            if line:
                ss = line.split()
                [P.tArray.append(x) for x in ss]
    if args['-a']:
        P.aVal = args['-a']

    add = False
    if args['-f']:
        ss = args['-f'].split(',')
        for s in ss:
            t_arr = s.split('-')
            if len(t_arr) ==1 :
                 P.outArrayId.append(int(t_arr[0]) -1)
            elif t_arr[1]:
                ss_n = list(map(int, t_arr))
                if(ss_n[0] <= ss_n[1]):
                    for k in range(ss_n[0],ss_n[1]+1):
                        P.outArrayId.append(k -1)
                else: #reverse order
                    for k in range(ss_n[0],ss_n[1]-1,-1):
                        P.outArrayId.append(k -1)
            else:
                P.outArrayId.append(int(t_arr[0]) -1)
                P.outArrayId.append(-1) # negative value indicates need to expand to all columns from
                                        # the starting point of P.outArrayId[-1].
    if args['-t']:
        add = True
        P.title = True
        P.First = False # -t mode, do not need expand.
        P.tArray = args['-t'].split(',')

    runApp()
