#!/usr/bin/env python3

"""

    -------------------------------------
    MatchCaseControlPCA
    -------------------------------------

    Usage:
        MatchCaseControlPCA.py -a casePCAfile -b controlPCAfile [-c weightFile] [-r]
        MatchCaseControlPCA.py -h | --help | -v | --version | -f | --format

    Options:
        -a casePCAfile     Case PCA output file.
        -b controlPCAfile  Control PCA output file.
        -c weightFile      Weight file, the proportion of variance explained by each PC.
        -r                 Repeating use control, default each control can only be used once.
        -h --help        Show this screen.
        -v --version     Show version.
        -f --format      Show input/output file format example.

    @Notes:
        1. Best match cases and controls based on the PCA results.
        2. Output matched results to stdout.
        3. Input format of PCA file: First column for name, second to N, for PCA dementional values.
            Name1   x   y   z   .....
            Name2   x   y   z   .....

           Input format for weights, signal line or line by line, total number equals the number of dementions:
            x y z

        4. Find an matching individual for case by minimize D = [(x_i-x_case)^2 + (y_i - y_case)^2 + ....],
            Iterate i for all controls.
        5. If weights have been assigned, use weighted distance.
            D = [(x_i-x_case)^2*w1 + (y_i - y_case)^2*w2 + ....]/(sum(w))

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
# intput PCA file:
#------------------------------------
Name1   x   y   z   .....
Name2   x   y   z   .....

# weight file:
# signal line or line by line, total number equals the number of dementions:
#------------------------------------
x y z ... N
    ''');

class P(object):
    case_f = '' # case file
    control_f = '' # control file.
    weight_f = '' #weight file
    RepeatingControl =  False

if __name__ == '__main__':
    args = docopt(__doc__, version='3.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    P.case_f = args['-a']
    P.control_f = args['-b']
    if args['-c']:
        P.weight_f = args['-c']
    if args['-r']:
        P.RepeatingControl = True

    controls = [] #[(name, [val1, val2]) , (name, [val1, val2])  ...]
    for line in open(P.control_f):
        line = line.strip()
        if line:
            ss = line.split()
            vals = list(map(float, ss[1:]))
            controls.append((ss[0], vals))

    weights = [] #weight for each demention, like the proportion of variance explained by each pc.
    if P.weight_f:
        with open(P.weight_f, 'r') as f:
            for line in f:
                [weights.append(float(x)) for x in line.strip().split()]

    def distance(vals1, vals2):
        '''Compute the sequared distance between point1 and point2'''
        if len(vals1) != len(vals2):
            sys.stderr.write('Error: Point1 and Point2 has different dimension:\n')
            sys.stderr.write('%s\n'%('\t'.join(map(str, vals1))))
            sys.stderr.write('%s\n'%('\t'.join(map(str, vals2))))
            sys.exit(-1)

        if weights:
            if len(vals1) != len(weights):
                sys.stderr.write('Error: PCA and weight has different dimension:\n')
                sys.exit(-1)
            else:
                return sum([(x-y)*(x-y)*z for x,y,z in zip(vals1, vals2, weights)])/sum(weights)

        else:
            return sum( [(x-y)*(x-y) for x,y in zip(vals1, vals2)])

    matchIds = set()
    def findMatch(case_values):
        '''Find the best match of controls for this case'''
        temp = []
        for names, vals in controls:
            temp.append((names, distance(case_values, vals)))
        #from small to large by distance
        temp = sorted(temp, key=lambda x: x[1])
        #print(temp)
        if P.RepeatingControl:
            return temp[0][0]
        else:
            for n, _ in temp:
                if n not in matchIds:
                    matchIds.add(n)
                    return n

        # all controls were used.
        return ''

    for line in open(P.case_f):
        line = line.strip()
        if line:
            ss = line.split()

            mname = findMatch(list(map(float, ss[1:])))
            if mname:
                sys.stdout.write('%s\t%s\n'%(ss[0], mname))
            else:
                sys.stderr.write('Can not find match for %s, all controls were used, please add more controls!\n'%(ss[0]))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
