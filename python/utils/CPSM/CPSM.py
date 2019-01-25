#!/usr/bin/env python3

'''

    Cross-phenotype spatial mapping.
    ref: Winsvold (2015) ‘Genetic analysis for a shared biological basis between migraine and coronary artery disease’, Neurology: Genetics, 1(1), pp. e10–e10. doi: 10.1212/NXG.0000000000000010.

    x = [-log(p) .... ], log tranformed p value for phenotype 1.
    y = [-log(p) .... ], log tranformed p value for phenotype 1.
    b = [.............], b is the physical position for the list of snps.

    for a focal snp n, the windnow of size 60kb, each side 30kb, snp as i,(i+1), ...n...j
    The raw weight for snp m is. 1 - abs(bm - bn)/(bj-bi).
    The normalized weight w  = wi/sum(W).
    The score for the focal snp n is: s = sum(w_i*x_i*y_i)/(1-sum(w_i^2)), acrossing index i.

    @Author: wavefancy@gmail.com, Wallace Wang.

    Usage:
        CPSM.py -p int,int -b int [--hw int] [--p1 int | --p2 int]
        CPSM.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. Add one or n (number of permutations) more columns for the computed scores.

    Options:
        -p int,int    Column index for the first and second GWAS pvalue. eg. 1,2
        -b int        Column index for physical position. eg. 3.
        --hw int      Half window size for testing the score in unit kb. default 30.
        --p1 int      Permute the first  GWAS int times, this will close the results for the original data.
        --p2 int      Permute the second GWAS int times, this will close the results for the original data.
        -h --help     Show this screen.
        --version     Show version.
        -f --format   Show input/output file format example.

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.
from docopt import docopt

def ShowFormat():
    '''File format example'''
    print('''
#Input file format(stdin)
------------------------
0.1 0.2 10000
0.01 0.3    20000
0.5 0.05    30000
0.1 0.2     40000
0.001 0.5   50000
0.01 0.01   80000

cat test.txt | python3 CPSM.py -p 1,2 -b 3 --hw 20
------------------------
0.100  0.20  10000  1.832773
0.010  0.30  20000  1.046518
0.500  0.05  30000  0.909536
0.100  0.20  40000  0.996895
0.001  0.50  50000  1.878862
0.010  0.01  80000  0.000000

cat test.txt | python3 CPSM.py -p 1,2 -b 3 --hw 20 --p2 3
------------------------
0.100  0.20  10000  1.500000  4.048455  2.735863
0.010  0.30  20000  0.856691  1.601321  1.960480
0.500  0.05  30000  1.813532  1.156956  1.807946
0.100  0.20  40000  2.943647  0.976667  2.298557
0.001  0.50  50000  9.975772  1.878862  4.645365
0.010  0.01  80000  0.000000  0.000000  0.000000
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    pcol = [int(x) -1 for x in args['-p'].split(',')]
    bcol = int(args['-b']) -1
    half_window_size = int(args['--hw']) if args['--hw'] else 30
    half_window_size *= 1000 # convert to unit kb.
    NO_PERMUT = True
    P1_PERMUTE = int(args['--p1']) if args['--p1'] else -1
    P2_PERMUTE = int(args['--p2']) if args['--p2'] else -1
    if P1_PERMUTE > 0 or P2_PERMUTE >0:
        NO_PERMUT = False

    import pandas as pd
    import numpy as np
    #load data from stdin
    data = pd.read_table(sys.stdin,header=None,delim_whitespace=True)
    p1 = np.log10(data.iloc[:, pcol[0]].values) * -1.0
    p2 = np.log10(data.iloc[:, pcol[1]].values) * -1.0
    pos = data.iloc[:, bcol].values

    def getWindowBoundary(index, pos_array, half_window_size):
        '''Get the window boundary for a focal snp at index
            both end included.
            return left,right
        '''
        left = max(0, index -1)
        while left >= 0:
            d = pos[index] - pos[left]
            if d >= half_window_size:
                if d > half_window_size:
                    left = left + 1
                break
            else:
                left = left -1
        left = max(0, left)

        right = index +1
        while right < len(pos_array):
            d = pos[right] - pos[index]
            if d >= half_window_size:
                if d > half_window_size:
                    right = right -1
                break
            else:
                right = right +1
        right = min(right, len(pos_array)-1)

        return left,right

    # computing score for each snp.
    def computingSscore(focal_index, left, right, p1 = p1, p2 =p2, pos=pos):
        ''''Computing sn socre for a given focal snp'''
        if left == right:
            return 0
        windnow_len = pos[right] - pos[left]
        w = np.array([1-abs(pos[focal_index]-pos[i])*1.0/windnow_len for i in range(left, right+1)])
        w_normal = w/sum(w)

        # Hadamard product, corresponding elements product
        top = p1[left:right+1] * p2[left:right+1] * w_normal
        bottom = w_normal * w_normal

        # print(f'L:{left}  R:{right} C:{focal_index}')
        # print(f'W: {w}')
        # print(f'w_normal {w_normal}')
        # print(f'bottom {bottom}')
        return np.sum(top) * 1.0 / (1-np.sum(bottom)) if 1-np.sum(bottom) != 0 else None

    #get all variant scores
    # Cache the boundary for permutation, only need calculate the boundary once.
    WIN_BOUNDARY_CACHE = []
    def getAllScores(p1=p1, p2=p2, pos=pos):
        all_score = []
        if not WIN_BOUNDARY_CACHE:
            for i in range(0, len(p1)):
                left, right = getWindowBoundary(i, pos, half_window_size)
                WIN_BOUNDARY_CACHE.append((left,right))

        for i in range(0, len(p1)):
            # left, right = getWindowBoundary(i, pos, half_window_size)
            left,right = WIN_BOUNDARY_CACHE[i]
            score = computingSscore(i, left, right, p1=p1, p2=p2, pos=pos)
            all_score.append(score)

        # print(f'All_scores: {all_score}')
        return all_score

    if NO_PERMUT:
        scores = getAllScores(p1=p1, p2=p2, pos=pos)
        #print output
        resuts = pd.concat([data, pd.DataFrame({'scores': scores})], axis=1, ignore_index=True)

    if P1_PERMUTE > 0:
        resuts = data
        for i in range(P1_PERMUTE):
            np.random.shuffle(p1)
            scores = getAllScores(p1=p1, p2=p2, pos=pos)
            resuts = pd.concat([resuts, pd.DataFrame({'scores_'+str(i): scores})], axis=1, ignore_index=True)

    if P2_PERMUTE > 0:
        resuts = data
        for i in range(P2_PERMUTE):
            np.random.shuffle(p2)
            scores = getAllScores(p1=p1, p2=p2, pos=pos)
            resuts = pd.concat([resuts, pd.DataFrame({'scores_'+str(i): scores})], axis=1, ignore_index=True)

    resuts.to_string(sys.stdout,header=False, index=False)
    sys.stdout.write('\n')
    
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
