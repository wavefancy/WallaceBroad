#!/usr/bin/env python

'''
    SubsetByKey

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Algorithms
    1. Include or exclude a subset of entries by keys.
    @Version 2.0
    1. Add the function to use multi-fields as key.
    @Version 2.1
    1. Add the option to indicate that the input file has title,
        Directly copy this line to stdout.
    @Version 3.0
    1. Add option to directly copy comment line.
        comment line started by '#'

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def help():
    sys.stderr.write('''
    -------------------------------------
    SubsetByKey
    -------------------------------------

    @Author: wavefancy@gmail.com
    @Version: 2.1

    @Usages:
    para1: key list file.(all of the fields in this file will be treated as key).
    para2: i|e, [include or exclude the key indicated entries in output].
    para3: Colum index to compare with keys.[start from 1, eg. 1,2,3|2]
    para[-t](optional): Indicate the fisrt line as title, directly copy to stdout.
    para[-c](optional): Directly copy comment lines to stdout. Comment line started with '#'.

    @Notes:
    1. Read from stdin and output to stdout.
    2. Combine multi-fileds by '-', then compare it against keys in key list file.
    -------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)

class P(object):
    key_file = ''
    action = '' #include or exclude
    cols = []     #Column index to compare with keys.
    title = False #Default no title.
    copyComment = False

if __name__ == '__main__':
    #check title.
    args = []
    for x in sys.argv:
        if x == '-t':
            P.title = True
        elif x == '-c':
            P.copyComment = True
        else:
            args.append(x)
    sys.argv = args

    if(len(sys.argv) != 4):
        help()

    P.key_file = sys.argv[1]
    P.action = sys.argv[2]
    if P.action != 'i' and P.action != 'e':
        sys.stderr.write('Please set a correct action on para2!\n')
        sys.exit(-1)
    for x in sys.argv[3].split(','):
        P.cols.append( int(x) -1)

    #read key sets.
    my_keys = set()
    for line in open(P.key_file):
        line = line.strip()
        if line:
            my_keys.add('-'.join(line.split()))

    maxSplit = max(P.cols) + 2
    for line in sys.stdin:
        line = line.strip()
        if line:
            if P.copyComment and line.startswith('#'):
                sys.stdout.write('%s\n'%(line))
                continue

            if P.title:
                sys.stdout.write('%s\n'%(line))
                P.title = False
            else:
                ss = line.split(None, maxSplit)
                ikeys = '-'.join([ss[x] for x in P.cols])

                if P.action == 'i':
                    if ikeys in my_keys:
                        sys.stdout.write('%s\n'%(line))
                else:
                    if ikeys not in my_keys:
                        sys.stdout.write('%s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
