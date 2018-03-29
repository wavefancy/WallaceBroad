#!/usr/bin/env python3

"""

    Refine the results output from annotateBEDbyGeneCDS.py

    1. Remove the gene name with dash if there is multiple hit of a record, eg:  RP1-317E23.6,SEPN1 ->SEPN1
    2. Match NA as its nearest record.
        17      7579699 7579721 TP53    TP53
        17      7579838 7579940 TP53    NA
        17      7580642 7580659 NA      NA
        17      8192106 8192183 RANGRF  RANGRF
        17      8192273 8192390 RANGRF  RANGRF
        -->
        17      7579699 7579721 TP53    TP53
        17      7579838 7579940 TP53    NA
        17      7580642 7580659 TP53      NA
        17      8192106 8192183 RANGRF  RANGRF
        17      8192273 8192390 RANGRF  RANGRF

    @Author: wavefancy@gmail.com

    Usage:
        annotateBEDbyGeneCDSRefine.py
        annotateBEDbyGeneCDSRefine.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.

    Options:
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
# INPUT
#----------------------
17      7579699 7579721 TP53    TP53
17      7579838 7579940 TP53    NA
17      7580642 7580659 NA      NA
17      8192106 8192183 RANGRF  RANGRF
17      8192273 8192390 RANGRF  RANGRF
11      61197618        61197654        RP11-286N22.8,SDHAF2    RP11-286N22.8,SDHAF2

# OUTPUT
#----------------------
17      7579699 7579721 TP53    TP53
17      7579838 7579940 TP53    NA
17      7580642 7580659 TP53    NA
17      8192106 8192183 RANGRF  RANGRF
17      8192273 8192390 RANGRF  RANGRF
11      61197618        61197654        SDHAF2  RP11-286N22.8,SDHAF2
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    posCOl = 2-1
    geneCOl = 4-1

    data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            gene = ss[geneCOl].split(',')

            # use the gene name without dash.
            if len(gene) != 1:
                for g in gene:
                    if g.find('-') == -1:
                        ss[geneCOl] = g
                        break

            ss[posCOl] = int(ss[posCOl])
            data.append(ss)

    # fill NA with its nearest nearby.
    def findNeighbor(i,data):
        results = []
        j = i -1
        while j >= 0:
            if data[j][0] != data[i][0]: #on different chromosome.
                j = -1
                break
            if data[j][geneCOl] != 'NA':
                break
            j = j -1
        results.append(j)
        j = i +1
        while j < len(data):
            if data[j][0] != data[i][0]: #on different chromosome.
                j = -1
                break
            if data[j][geneCOl] != 'NA':
                break
            j = j +1
        results.append(j)
        return results

    #update NA
    import math
    for i in range(len(data)):
        d = data[i]
        if d[geneCOl] == 'NA':
            neighbor = findNeighbor(i,data)
            left = data[neighbor[0]][posCOl] if neighbor[0] > 0 else math.inf
            right = data[neighbor[1]][posCOl] if neighbor[1] > 0 else math.inf

            if abs(left - d[posCOl]) <= abs(right - d[posCOl]):
                d[geneCOl] = data[neighbor[0]][geneCOl]
            else:
                d[geneCOl] = data[neighbor[1]][geneCOl]

    #output results
    for d in data:
        sys.stdout.write('%s\n'%('\t'.join(map(str,d))))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
