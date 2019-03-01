#!/usr/bin/env python3

'''

    Collapse SNPs into regions defined by leading SNP (smallest pvalue).

    @Author: wavefancy@gmail.com, Wallace Wang.

    Usage:
        CollapseByLeadingSNP.py [-d int]
        CollapseByLeadingSNP.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
              Add one column for indicating belongs to which leading snp.
        2. Read three columns from stdin, chr-bp-pvalue, sorted by chr and then by pvalue (small to large).

    Options:
        -d int        The flanking distance around the leading snp, default 500000.
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
#Input file format(stdin), sorted by CHR and then P value (small to large).
------------------------
CHR     BP      P
1       150510660       5.26e-13
1       38386727        1.06e-11
1       2990994 7.09e-10
1       2192948 5.7e-08
10      44480811        2.97e-20
10      96019501        4.79e-14
10      124230750       1.58e-13
10      104697781       1.51e-11
10      124060802       1.02e-10
10      124199016       1.58e-10
10      124236756       9.73e-09
10      82203663        1.26e-08
11      103673294       1.56e-23
11      9751780 9.57e-13
11      65349063        3.31e-09
11      16513512        1.29e-08

#cat test.txt | python3 Combinations4Row.py -n 2
------------------------
1;2
1;3
2;3
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    F_Distance = int(args['-d']) if args['-d'] else 500000


    data_map = {}
    for line in sys.stdin:
        line = line.strip()
        if line :
            ss = line.split()
            try:
                ss[1] = int(ss[1])
                ss[2] = float(ss[2])

                # only add validated values.
                if ss[0] not in data_map:
                    data_map[ss[0]] = []
                data_map[ss[0]].append(ss)

            except Exception as e:
                pass

    #print(data_map)
    out = []
    # check region and output.
    while len(data_map.keys()) >0:
        r_keys = []

        for key in data_map.keys():
            data = data_map[key]
            data[0].append(data[0][1])
            out.append(data[0])

            removed = set([0])
            for i in range(1,len(data)):
                if abs(data[i][1]-data[0][1]) <= F_Distance:
                    data[i].append(data[0][1])
                    out.append(data[i])
                    removed.add(i)

            new_data = [d for i,d in enumerate(data) if i not in removed]
            if new_data:
                data_map[key] = new_data
            else:
                r_keys.append(key)

        # remove keys no data associated it.
        for r in r_keys:
            del data_map[r]

    #print(out)
    out = sorted(out,key=lambda x:(x[0],x[2]))
    for o in out:
        sys.stdout.write('%s\n'%('\t'.join(map(str,o))))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
