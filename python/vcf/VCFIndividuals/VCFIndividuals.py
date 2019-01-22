#!/usr/bin/env python3

'''
    VCFIndividuals

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Algorithms:
        Extract VCF individuals from VCF file.
    @Version 2.0
        Add function to remove individuals.
    @Version 3.0
        1. Change parameter setting, skip set meta info.
        2. Check duplicate ids.
    @Version 4.0
        1. Improve the performance for finding individuals in input vcf.

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def help():
    sys.stderr.write('''
    -------------------------------------
    VCFIndividuals
    -------------------------------------

    @Author: wavefancy@gmail.com
    @Version: 4.0

    @Usages
    para1: individual id list file (line by line or sep. by '\t').
    para2:[-r, optional] remove individuals from the stdout.
    para:[-i, optional] ignore those individuals can not found in vcf file.

    @Notes:
    1. Read VCF file from stdin and output to stdout.
    2. *** Output will be reordered as the order in the id list file. ***
    -------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)

class P(object):
    skipCol = 0
    idFiles = ''

    remove = False

if __name__ == '__main__':
    args = []
    IGNORE_ID = False
    for x in sys.argv:
        if x == '-r':
            P.remove =  True
        elif x == '-i':
            IGNORE_ID = True
        else:
            args.append(x)

    sys.argv = args
    if(len(sys.argv) != 2):
        help()

    #P.skipCol = int(sys.argv[1])
    P.skipCol = 9
    P.idFiles = sys.argv[1]

    #read id tags.
    ids = []
    idset=set()
    for line in open(P.idFiles):
        line = line.strip()
        if line:
            for x in line.split():
                if x in idset:
                    sys.stderr.write('Warning: duplicate name in id list file, only use the first one: %s\n'%(x))
                else:
                    ids.append(x)
                    idset.add(x)

    #process seq. data.
    output = False
    idIndex = []
    for x in range(0, P.skipCol):
        idIndex.append(x)

    temp_idis = []
    maxSplit = 0
    for line in sys.stdin:
        line = line.strip()
        if line:
            if output:
                #output results.
                ss = line.split(None, maxSplit)
                sys.stdout.write('%s\n'%('\t'.join([ss[x] for x in idIndex])))

            else:
                if line.startswith('##'):
                    sys.stdout.write('%s\n'%(line))
                elif line.startswith('#C') or line.startswith('#c'):
                    output = True
                    ss = line.split()

                    #update the performance for find individuals.
                    INDMAP = {}
                    for x,y in zip(range(len(ss)),ss):
                        if y in INDMAP:
                            sys.stderr.write('ERROR: duplicate ids in input vcf: %s\n'%(y))
                            sys.exit(-1)
                        else:
                            INDMAP[y] = x

                    for x in ids:
                        try:
                            ii = INDMAP[x]
                            temp_idis.append(ii)
                        except KeyError:
                            if IGNORE_ID:
                                sys.stderr.write('***WARN: Can not find individual from vcf for: %s\n'%(x))
                            else:
                                sys.stderr.write('***Can not find individual from vcf for: %s\n'%(x))
                                sys.stderr.write('***System exited, please check!\n')
                                sys.exit(-1)

                    if P.remove: #remove mode.
                        temp_idis = [x for x in range(P.skipCol, len(ss)) if x not in temp_idis]

                    idIndex = idIndex + temp_idis
                    #mm = max(idIndex)
                    #for title.
                    sys.stdout.write('%s\n'%('\t'.join([ss[x] for x in idIndex])))
                    maxSplit = max(idIndex) + 2

    sys.stdout.flush()
    sys.stderr.flush()
    sys.stdout.close()
    sys.stderr.close()
