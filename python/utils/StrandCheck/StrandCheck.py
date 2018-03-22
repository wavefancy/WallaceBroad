#!/usr/bin/env python

'''
    StrandCheck

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Algorithms:

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def help():
    sys.stderr.write('''
    -------------------------------------
    StrandCheck
    -------------------------------------

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Usages:
    para1: input file1.
    para2: input file2.
    para3: key column index for input file.
    para4: column index for allele1.
    para5: column index for allele2.

    @Notes:
    1. Check the allele between two input files.
        1.1 Output those sites which need allele flip in stdout.
        1.2 Output those sites even allele flipping can't solve the problem to stderr.
        1.3 Only check the common SNPs between two files[compare by key], skip private SNPs.
        1.4 key should be uniq in both input files.
    2. Align output as order file1_content|||file2_content.
    3. Column index starts from 1.
    -------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)

class P(object):
    file1 = ''
    file2 = ''
    col_key = -1
    col_a1 = -1
    col_a2 =-1

if __name__ == '__main__':
    if len(sys.argv) != 6:
        help()

    P.file1 = sys.argv[1]
    P.file2 = sys.argv[2]
    P.col_key = int(sys.argv[3]) -1
    P.col_a1 = int(sys.argv[4]) -1
    P.col_a2 = int(sys.argv[5]) -1

    c_map = {} #snpid - content array
    for line in open(P.file2):
        line = line.strip()
        if line:
            ss = line.split()
            if ss[P.col_key] in c_map:
                sys.stderr.write('ERROR: in "%s", duplicate key ID: %s\n'%(P.file1, ss[P.col_key]))
                sys.exit(-1)
            c_map[ss[P.col_key]] = ss

    id_set = set()
    flip_map = {'A':'T', 'T':'A', 'G':'C','C':'G', '0':'0', 'N':'N'}

    def flip(string):
        '''flipping strand, flip or keep the sample if the allele code is out-of-control.'''
        return ''.join([flip_map.get(x,x) for x in string])

    def compareTwoAllele(allele1, allele2):
        '''check if two alleles are equal, 0/N equal with every allele'''
        if allele1 == '0' or allele2 == '0' or allele1 == 'N' or allele2 == 'N':
            return True;
        else:
            return allele1 == allele2

    def compareAlleleSet(set1, set2):
        '''Compare if the two alleles in the two input sets are matching'''
        return ( compareTwoAllele(set1[0], set2[0]) and compareTwoAllele(set1[1], set2[1])) or ( compareTwoAllele(set1[0], set2[1]) and compareTwoAllele(set1[1], set2[0]))

    for line in open(P.file1):
        line = line.strip()
        if line:
            ss = line.split()
            if ss[P.col_key] in id_set:
                sys.stderr.write('ERROR: in "%s", duplicate key ID: %s\n'%(P.file2, ss[P.col_key]))
                sys.exit(-1)
            id_set.add(ss[1])

            try:
                # if ss[P.col_key] == '1:103213499':
                #     print(ss)
                ss2 = c_map[ss[P.col_key]]

                arr1 = (ss[P.col_a1].upper(),  ss[P.col_a2].upper())
                arr2 = (ss2[P.col_a1].upper(), ss2[P.col_a2].upper())
                # print(arr1)
                #print(arr2)

                if compareAlleleSet(arr1, arr2): # do not need flip.
                    # print('yes')
                    continue

                elif compareAlleleSet(arr1, (flip(arr2[0]), flip(arr2[1]))): # flip then match.
                    # print('flip')
                    sys.stdout.write('%s|||%s\n'%('\t'.join(ss), '\t'.join(ss2)))

                else: #flip even can't mach.
                    # print('fail')
                    sys.stderr.write('%s|||%s\n'%('\t'.join(ss), '\t'.join(ss2)))

            except KeyError:
                # print('error')
                pass

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
