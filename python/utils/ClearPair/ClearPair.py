#!/usr/bin/env python

"""

    Remove one individual from each pair input, use gready optimization approach
        to remove as less individual as possible. Preferentially remove individual
        who involved in multiple input pairs.
    *** Check kFIle/rFIle, when input id pairs.

    @Author: wavefancy@gmail.com

    Usage:
        ClearPair.py [-k kFile] [-r rFile]
        ClearPair.py -h | --help | -v | --version | -f | --format

    Notes:
        Read id pairs from stdin and output removed ids to stdout.

    Options:
        -k kFile      Try best to keep individuals deleared in this file.
        -r rFile      First priority to remove individuals delceared in this file.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.
from docopt import docopt

def ShowFormat():
    '''File format example'''
    print('''
    #Input file format(stdin), first two columns as id pair, ignore other columns.
    ------------------------
    ID1 ID2
    ID3 ID4

    #kFile/rFile, one id per line.
    ------------------------
    ID2
    ID3
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='2.0')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    def readIds(iFile):
        '''Read id from file, one line one id. RETURN set for ids.'''
        rr = set()
        for line in open(iFile, 'r'):
            line = line.strip()
            if line:
                rr.add(line)
        return rr

    kIDs = set()
    rIDs = set()
    out_a = []  #output array
    if args['-k']:
        kIDs = readIds(args['-k'])
    if args['-r']:
        rIDs = readIds(args['-r'])

    def checkKeepPair(ss):
        '''Check Keep Pair
        ss: a pair, two elements.
        Return True: one element was add in out_a.
        Return False: for later check, not action operated.
        '''
        if kIDs:
            if ss[0] in kIDs and (ss[1] not in kIDs):
                out_a.append(ss[1])
                return True
            if ss[0] not in kIDs and ss[1] in kIDs:
                out_a.append(ss[0])
                return True
        return False

    def checkRemovePair(ss):
        '''Check Keep Pair
        ss: a pair, two elements.
        Return True: one element was add in out_a.
        Return False: for later check, not action operated.
        '''
        if rIDs:
            if ss[0] in rIDs and ss[1] not in rIDs:
                out_a.append(ss[0])
                return True
            if ss[1] in rIDs and ss[0] not in rIDs:
                out_a.append(ss[1])
                return True
        return False

    pair_map = dict() # name -> [name1, name2]
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()

            # Check priority files.
            if kIDs:
                if checkKeepPair(ss):
                    continue
            if rIDs:
                if checkRemovePair(ss):
                    continue

            if ss[0] not in pair_map:
                pair_map[ss[0]] = []
            pair_map[ss[0]].append(ss[1])

            if ss[1] not in pair_map:
                pair_map[ss[1]] = []
            pair_map[ss[1]].append(ss[0])

    def removeOne(mm):
        '''Remove one entry from the intput map(mm),
            return the key of the removed entry if successfully.
            return None if failed, then no paired individuals existed.
        '''
        if len(mm) == 0:
            return None

        kk = sorted(mm.keys(), key = lambda x: len(mm[x]), reverse=True)
        if len(mm[kk[0]]) >= 1:
            id1 = kk[0]
            for x in mm[id1]:
                try: #reverse connection may not hold.
                    mm[x].remove(id1)
                except KeyError:
                    pass

            del mm[id1]

            return id1
        else:
            return None


    t_k = removeOne(pair_map)
    #print p_map
    while t_k != None:
        out_a.append(t_k)
        t_k = removeOne(pair_map)

    sys.stdout.write('%s\n'%('\n'.join(out_a)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
