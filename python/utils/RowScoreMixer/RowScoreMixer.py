#!/usr/bin/env python3

"""

    Mix scores from different rows by its weight, output the weighted sum of scores.

    @Author: wavefancy@gmail.com

    Usage:
        RowScoreMixer.py -w file
        RowScoreMixer.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read scores from stdin, and output results to stdout.
        2. Input format: 
            * 1st line is tittle. 
            * the 1st col is name, used to associate weight, from 2-n are scores. 
        3. Output format: 
            * 1st colum: NumberOfGenesHasScore:GeneNames:Weights, 2-n are the combined scores.
            * Genes don't have score associated with it, the output weight will be 'NA'.
            * If less than one gene in the network has scores, the mixed scores were all 'NA'.
        4. See example by -f.

    Options:
        -w file        weight file, define how to compute the weighted sum scores.
                            FORMAT: name1:weight1 name2:weight2 ...
        -h --help      Show this screen.
        -v --version   Show version.
        -f --format    Show input/output file format example.
            
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def ShowFormat():
    '''Input File format example:'''
    print('''
# INPUT:
------------------------
Gene    NA1 NA2
N1      1 2
N2      2 3
N3      1 5

# WEIGHT:
------------------------
N1:1 N2:3
N2:2 N3:4
N2:2 N4:4

#OUTPUT:
cat test.txt | python3 ./RowScoreMixer.py -w weight.txt 
------------------------
NumberOfGenesHasScore:GeneNames:Weights NA1 NA2
2:N1,N2:1,3     7       11
2:N2,N3:2,4     8       26
1:N2,N4:2,NA    NA      NA
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    # loading the scores.
    score_map = {}
    Fill_NAs = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split(None,1)
            if Fill_NAs:
                if ss[0] in score_map:
                    sys.stderr.write('ERROR: duplicated gene name in score file: %s\n'%(ss[0]))
                    sys.exit(-1)
                else:
                    score_map[ss[0]] = ss[1]
            else:
                ss = line.split(None,1)
                sys.stdout.write('NumberOfGenesHasScore:GeneNames:Weights\t%s\n'%(ss[1]))
                Fill_NAs = '\t'.join(['NA' for x in ss[1].split()])
  
    import numpy as np
    with open(args['-w'], 'r') as nfile:
        for line in nfile:
            line = line.strip()
            if line:
                ss = line.split()

                name = []
                weight = []
                out_name = []
                out_weight = []
                for x in ss:
                    xx = x.split(':')

                    out_name.append(xx[0])
                    if xx[0] in score_map: # only put in genes we have score for it.
                        name.append(xx[0])
                        weight.append(xx[1])
                        out_weight.append(xx[1])
                    else:
                        out_weight.append('NA')

                if len(name) <= 1:
                    s = Fill_NAs
                else:
                    # compute the weighted sum.
                    t_sum = np.array([float(x) for x in score_map[name[0]].split()]) * float(weight[0])
                    for g,w in zip(name[1:], weight[1:]):
                        tt = np.array([float(x) for x  in score_map[g].split()]) * float(w)
                        t_sum = t_sum + tt
                    
                    s = '\t'.join(['%g'%(x) for x in t_sum])

                n = ','.join(out_name)
                ww = ','.join(out_weight)
                sys.stdout.write('%d:%s:%s\t%s\n'%(len(name),n,ww,s))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
