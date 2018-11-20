#!/usr/bin/env python3

"""

    Extract exon regions from refSeq gene format.

    @Author: wavefancy@gmail.com

    Usage:
        ExonRegionsFromRefSeq.py [-p padding]
        ExonRegionsFromRefSeq.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output bed format results to stdout.
        2. Aggregate all regions from all the transcripts of a gene, padding each
           exon '-p padding' number of bases. Automatic merge region if they are
           overlapped together.
        3. Read 4 colums from stdin: 'contigName, exonStarts, exonEnds, geneName'
        4. See example by -f.

    Options:
        -p padding    The number of bases padded for each exon regions, (Default: 100).
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

    Dependency:
        https://github.com/intiocean/pyinter
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    #'contigName, exonStarts, exonEnds, geneName'
    ------------------------
chr16   30395111,30395779,30397329, 30395578,30395873,30400108, ZNF48
chr1    101,120    110,130   T1
chr1    115  150  T1

    #output: contigName, regionStart, regionEnd, geneName+regionID.
    ------------------------
chr16   30395010        30395973        ZNF48+1
chr16   30397228        30400208        ZNF48+2
chr1    0       250     T1+1
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    padding = 100
    if args['-p']:
        padding = int(args['-p'])

    from collections import OrderedDict
    dataMap = OrderedDict() # name[contigName+geneName] -> (contigName, geneName, IntervalSet)
    from pyinter import interval, interval_set
    # https://github.com/intiocean/pyinter

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            exonStart = ss[1].strip(',').split(',')
            exonEnd = ss[2].strip(',').split(',')

            name = ss[0] + ss[3]
            if name not in dataMap:
                dataMap[name] = (ss[0], ss[3], interval_set.IntervalSet())

            for s, e in zip(exonStart, exonEnd):
                s = int(s) -1 - padding # bed file 0 based.
                if s < 0:
                    s = 0
                e = int(e) + padding # end not include, therefore do not need -1.
                #automatic merge overlapped interval.
                dataMap[name][2].add(interval.closed(s, e)) #auto aggregate overlap.

    #output results.
    for _,v in dataMap.items():
        index = 0
        for i in v[2]:
            index += 1
            sys.stdout.write('%s\t%d\t%d\t%s+%d\n'%(v[0], i.lower_value, i.upper_value, v[1], index))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
