#!/usr/bin/env python3

"""

    Calculate the genotye concordance between call set.
    @Author: wavefancy@gmail.com

    Usage:
        GenotypeConcordance.py -s file -c int [-i]
        GenotypeConcordance.py -h | --help | -v | --version | -f

    Notes:
        1. Read input file from stdin. Output summary to stdout.


    Options:
        -s file       Sample pair files, two columns.
                            Sample name for true set, Sample name for call set.
        -c int        Column index for data start, index starts from 1.
        -i            Get summary at individual level, default at site level.
        -v --version  Show version.
        -f --format   Show format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''File format example'''
    print('''
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)
    if args['--format']:
        ShowFormat()
        sys.exit(-1)

    d_col = int(args['-c']) -1
    samplePairIndex = [] #()
    samples = []
    sitesModel = False if args['-i'] else True
    with open(args['-s'],'r') as sfile:
        for line in sfile:
            line = line.strip()
            if line:
                samples.append(line.split())

    def getIndex(array, val):
        '''Get the index for val in an array'''
        try:
            x = array.index(val)
        except ValueError:
            sys.stderr.write('ERROR: can not find this sample in input: %s\n'%(val))
            sys.exit(-1)
        return x

    def getGeno(val):
        if val[0] == '.':
            return '.'
        else:
            if val[0] < val[2]:
                return val[0] + val[2]
            else:
                return val[2] + val[0]

    title = []
    data = []
    from collections import OrderedDict
    for line in sys.stdin:
        line = line.strip()
        if line:
            if not title:
                title = line.split()
                #check index for each sample pair.
                ss = set(title[d_col:])
                if len(ss) != len(title[d_col:]):
                    system.error.write('ERROR: duplicate sample names in the input, please check!\n')
                    system.exit(-1)
                samplePairIndex = [(getIndex(title,x),getIndex(title,y)) for x,y in samples]

                if sitesModel:
                    out = title[:d_col]
                    for x in ['00','01','11']:
                        out.append('correct_'+x)
                    for x in ['00','01','11']:
                        out.append('error_'+x)
                    sys.stdout.write('%s\n'%('\t'.join(out)))
                else:
                    out = ['true_sample','call_sample']
                    for x in ['00','01','11']:
                        out.append('correct_'+x)
                    for x in ['00','01','11']:
                        out.append('error_'+x)
                    for x in ['00','01','11']:
                        out.append('errorRate_'+x)

                    out.append('errorRateNonREFHOMO')
                    out.append('errorRateTotal')
                    sys.stdout.write('%s\n'%('\t'.join(out)))

            else:
                ss = line.split()
                if sitesModel:
                    # missing = 0
                    correctMap = OrderedDict()
                    correctMap['00'] = 0
                    correctMap['01'] = 0
                    correctMap['11'] = 0

                    wrongMap = OrderedDict()
                    wrongMap['00'] = 0
                    wrongMap['01'] = 0
                    wrongMap['11'] = 0

                    for x,y in samplePairIndex:
                        gx = getGeno(ss[x])
                        gy = getGeno(ss[y])
                        if gx == '.' or gy == '.':
                            continue
                        # if gy == '.':
                        #     missing += 1
                        if gx == gy:
                            correctMap[gx] = correctMap[gx] +1
                        else:
                            wrongMap[gx] = wrongMap[gx] +1
                    #output the return for a sites.
                    out = ss[:d_col]
                    for _,v in correctMap.items():
                        out.append(str(v))
                    for _,v in wrongMap.items():
                        out.append(str(v))

                    sys.stdout.write('%s\n'%('\t'.join(out)))
                else:
                    data.append(ss)

    #output for individual model
    if not sitesModel:
        for i in range(len(samplePairIndex)):
            x,y = samplePairIndex[i]

            correctMap = OrderedDict()
            correctMap['00'] = 0
            correctMap['01'] = 0
            correctMap['11'] = 0

            wrongMap = OrderedDict()
            wrongMap['00'] = 0
            wrongMap['01'] = 0
            wrongMap['11'] = 0

            for d in data:
                gx = getGeno(d[x])
                gy = getGeno(d[y])

                if gx == '.' or gy == '.':
                    continue
                # if gy == '.':
                #     missing += 1
                if gx == gy:
                    correctMap[gx] = correctMap[gx] +1
                else:
                    wrongMap[gx] = wrongMap[gx] +1

            #output results.
            out = [samples[i][0], samples[i][1]]
            corr = []
            wrong = []
            for _,v in correctMap.items():
                out.append(str(v))
                corr.append(v)
            for _,v in wrongMap.items():
                out.append(str(v))
                wrong.append(v)

            #output error rate:
            for m,n in zip(corr,wrong):
                if m+n == 0:
                    out.append('NA')
                else:
                    out.append('%.4e'%(n*1.0/(m+n)))

            #errorRate non ref homo.
            wrong1 = wrong[1:]
            corr1 = corr[1:]
            out.append('%.4e'%(sum(wrong1)*1.0/(sum(wrong1)+sum(corr1))))
            #errorRate total
            out.append('%.4e'%(sum(wrong)*1.0/(sum(wrong)+sum(corr))))
            sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
