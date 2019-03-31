#!/usr/bin/env python3

'''
    CheckDuplicateByKey

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Algorithms:
        1. Check duplicate by user specified keys.

    @Version: 1.1
        1. Add the funcion to close output duplicated lines.
'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def help():
    sys.stderr.write('''
    -------------------------------------
    CheckDuplicateByKey
    -------------------------------------

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @para1: keys (eg. -k1,5, -k2-6, -k3).
    @para2: [a|f|e|x] (action1 for duplicated lines: see notes)
    @para3: [y|n] (action2 for uniq lines: yes[y] or not[n] output uniq records.)
    @optional: -s, skip compare comment lines, comment started by #.
               -c, skip compare comment lines, directly copy comment lines to stdout, BEFORE output other content.
    @para[-h]: display help.

    @Notes:
    1. Read data from stdin (no presorting needed), and output to stdout.
    2. Column index starts from 1.
    3. Action1:
        a: output all duplicated lines.
        f: output the first record of each duplicated entry.
        e: output all records, but except the first record of each duplicated entry.
        x: do not output duplicated lines.
    -------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)

if __name__ == '__main__':
    skipComments = False
    copy = False
    args = []
    for x in sys.argv:  #check -s flag.
        if x == '-s':
            skipComments = True
        elif x == '-c':
            skipComments = True
            copy = True
        else:
            args.append(x)
    sys.argv = args

    if len(sys.argv) != 4:
        help()
    if sys.argv[2] not in set(['a','f','e','x']):
        sys.stderr.write('*** Please set correct parameter for para2, lower case!\n')
        help()
    if sys.argv[3] not in set(['y','n']):
        sys.stderr.write('*** Please set correct parameter for para3, lower case!\n')
        help()

    # get key lists
    x = sys.argv[1]
    kk = []
    if x.startswith('-k'):
        x = x[2:]
        ss = x.split(',')
        for s in ss:
            temp = s.split('-')
            if len(temp) == 1:
                kk.append(int(temp[0]))
            else:
                for i in range(int(temp[0]), int(temp[1]) +1):
                    kk.append(i)
    else:
        help()
    #shift to 0 based.
    kk = [x-1 for x in kk]

    def getKey(s_arr, key_Index):
        '''Combine muti-column keys'''
        rr = [ s_arr[x] for x in key_Index]
        return ','.join(rr)

    contents = []
    key_map = {}
    for line in sys.stdin:
        line = line.strip()
        if line:
            if skipComments and line.startswith('#'):
                #print(copy)
                if copy:
                    sys.stdout.write('%s\n'%(line))
                continue

            ss = line.split()
            key = getKey(ss, kk)
            if key in key_map:
                key_map[key] = key_map[key] + 1
            else:
                key_map[key] = 1

            contents.append((key,line))

    #output results.
    d_set = set() #cache the duplicated keys.
    for x in contents:
        if key_map[x[0]] == 1:
            if sys.argv[3] == 'y': #output uniq records
                sys.stdout.write('%s\n'%(x[1]))

        else:
            if sys.argv[2] == 'a':
                sys.stdout.write('%s\n'%(x[1]))
            elif sys.argv[2] == 'f':
                if x[0] not in d_set:
                    d_set.add(x[0])
                    sys.stdout.write('%s\n'%(x[1]))
            elif sys.argv[2] == 'e': #sys.argv[2] == 'e': not the first records.
                if x[0] in d_set:
                    sys.stdout.write('%s\n'%(x[1]))
                else:
                    d_set.add(x[0])
            else: #sys.argv[2] == 'x': do not output duplicated lines to output.
                pass

    sys.stdout.flush()
    sys.stdout.close()
