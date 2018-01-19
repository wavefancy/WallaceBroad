#!/usr/bin/env python3

"""

    Calculate the category genotype concordance summary statistics.

    @Author: wavefancy@gmail.com

    Usage:
        GCCategorySummay.py
        GCCategorySummay.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output results to stdout.

    Options:
        -a int        Column index for the first(ref) allele, index starts from 1.
        -b int        Column index for the second(alt) allele.
        -c            Skip comment checking line, comment line started by '#'
        -r            Remove AT, GC sites, while keep all the other content.
                      Otherwise output AT/GC sites, default.
        -m            Output comment line, default false.
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
    # -a 5 -b 6
    ------------------------
1       1:82154 0       82154   T       A
1       1:752566        0       752566  C       G
1       1:752721        0       752721  G       A

    #output:
    ------------------------
1       1:82154 0       82154   T       A
1       1:752566        0       752566  C       G
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    from collections import OrderedDict
    dataMap = OrderedDict()
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                dd = [int(x) for x in ss[1:]]
                if ss[0] not in dataMap:
                    dataMap[ss[0]] = []
                dataMap[ss[0]].append(dd)
            except ValueError:
                sys.stderr.write('WARN: parse value error: %s\n'%(line))

    #output summary statistics
    import numpy
    sys.stdout.write('Label\tcorrect_00\tcorrect_01\tcorrect_11\terror_00\terror_01\terror_11\terrorRate_00\terrorRate_01\terrorRate_11\terrorRate_nonREFHomo\terrorRate_Total\n')
    # print(dataMap)
    for k,v in dataMap.items():
        # print(v)
        sm = numpy.sum(v,axis=0)
        out = [k]
        [out.append('%d'%(x)) for x in sm]
        cor = sm[:3]
        err = sm[3:]
        for m,n in zip(cor,err):
            if m+n == 0:
                out.append('NA')
            else:
                out.append('%.4e'%(n*1.0/(m+n)))

        cor1 = cor[1:]
        err1 = err[1:]
        out.append('%.4e'%(sum(err1)*1.0/(sum(err1)+sum(cor1))))

        out.append('%.4e'%(sum(err)*1.0/(sum(err)+sum(cor))))
        sys.stdout.write('%s\n'%('\t'.join(out)))


sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
