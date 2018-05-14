#!/usr/bin/env python

"""

    Do PCA analysis.

    @Author: wavefancy@gmail.com

    Usage:
        PCA.py [-l] -n int
        PCA.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout.
        2. Output results from stdout.

    Options:
        -l            Indicate first column as title, default False.
        -n int        Number of PCs to decompose.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
#   Ref:
#        1. https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
#
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''Input File format example:'''
    print('''
#input example
------------------------
Y 1  2  3  4  3  4  5  4  5  5  4  5  4  5  4  5  6  5  4  5  4  3  4
T 4  2  3  4  5  4  5  6  7  4  8  9  8  8  6  6  5  5  5  5  5  5  5
M 4  1  2  3  4  5  6  7  5  8  7  8  7  8  7  8  7  7  7  7  7  6  5
K 4  1  2  5  6  7  8  9  7  8  7  8  7  7  7  7  7  7  6  6  4  4  4

#cat test.txt | wcut -f2- | python3 PCA.py -n 3
------------------------
ExplainedVar    0.5660  0.2364  0.1976
Sample  PC1     PC2     PC3
0       5.5742e+00      -1.4207e+00     1.0485e+00
1       7.9032e-01      3.3549e+00      -2.0023e+00
2       -3.4264e+00     8.5029e-01      2.9886e+00
3       -2.9381e+00     -2.7845e+00     -2.0348e+00

#cat test.txt | wcut -f2- | python3 PCA.py -n 3
------------------------
ExplainedVar    0.5660  0.2364  0.1976
Sample  PC0     PC1     PC2
Y       5.5742e+00      -1.4207e+00     1.0485e+00
T       7.9032e-01      3.3549e+00      -2.0023e+00
M       -3.4264e+00     8.5029e-01      2.9886e+00
K       -2.9381e+00     -2.7845e+00     -2.0348e+00
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    FIRSTLABLE = True if args['-l'] else False
    NUM_PC     = int(args['-n'])

    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA

    if FIRSTLABLE:
        data = pd.read_table(sys.stdin,header=None,delim_whitespace=True,index_col=0)
    else:
        data = pd.read_table(sys.stdin,header=None,delim_whitespace=True)

    std_data = StandardScaler().fit_transform(data)
    # print(std_data[:,0:5])
    pca = PCA(n_components=NUM_PC)
    pcs = pca.fit_transform(std_data)

    # print(pca.explained_variance_ratio_)
    out = ['ExplainedVar']
    [out.append('%.4f'%(x)) for x in pca.explained_variance_ratio_]
    sys.stdout.write('%s\n'%('\t'.join(out)))

    out = ['Sample']
    [out.append('PC%d'%(x+1)) for x in range(NUM_PC)]

    sys.stdout.write('%s\n'%('\t'.join(out)))
    for s,dd in zip(data.index,pcs):
        out = [str(s)]
        [out.append('%.4e'%(x)) for x in dd]
        sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
