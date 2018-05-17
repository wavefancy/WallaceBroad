#!/usr/bin/env python

'''
    CategoryExtreme

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Algorithms:
    1. Find out the extreme value for each category.

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def help():
    sys.stderr.write('''
    -------------------------------------
    CategoryExtreme
    -------------------------------------

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Usages:
    para1: Column index for category name.
    para2: Column index for values.
    para3: [i|x] output the line with the minimum(i) or maximum(x) value.

    @Notes:
    1. Read data from stdin and output to stdout.
    2. Entries of the same category should be put in adjacent lines.
        -----Exameple-------
        s1  12
        s1  13
        s2  34
        ..........
    3. If content(value) can't be converted to float, copy this line to stderr.
    4. Column index starts from 1.
    -------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)

class P:
    col_c = -1 # Column index for category. permit multi-columns as category.
    col_v = -1 # Column index for values.
    min_v = True # True for minimum, False for maximum

if __name__ == '__main__':
    if len(sys.argv) != 4:
        help()

    #P.col_c = int(sys.argv[1]) -1
    P.col_c = [int(x)-1 for x in sys.argv[1].split(',')] #column starts from 1.
    P.col_v = int(sys.argv[2]) -1
    if sys.argv[3].lower() == 'x':
        P.min_v = False


    def processOne(entries):
        '''find out the extreme value and output'''
        ee = ''
        vv = []
        # print(entries)
        for _,x in entries: #skip entry name.
            try:
                t_vv = float(x[P.col_v])

                if vv:
                    if P.min_v:
                        if t_vv < vv[0]:
                            vv[0] = t_vv
                            ee = x
                    else:
                        if t_vv > vv[0]:
                            vv[0] = t_vv
                            ee = x
                else:
                    vv.append( t_vv )
                    ee = x

            except ValueError:
                sys.stderr.write('%s\n'%('\t'.join(x)))
        if ee:
            sys.stdout.write('%s\n'%('\t'.join(ee)))

    #read from stdin.
    c_temp = [] #[(entryName,entry1), (entryName,entry2)... ] #entries for a category.
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            name = ','.join([ss[x] for x in P.col_c])
            if c_temp:
                if c_temp[-1][0] == name:
                    c_temp.append((name,ss))
                else:
                    processOne(c_temp)
                    c_temp = []
                    c_temp.append((name,ss))
            else:
                c_temp.append((name,ss))

    #deal with the last category.
    processOne(c_temp)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
