#!/usr/bin/env python

"""

    Generate statistics for each row/category.
    *** IF run in category model, the same category should be sorted in together.

    @Author: wavefancy@gmail.com

    Usage:
        RowStatistics.py [-c] [--set int] [--min int] [--max int] [--mean] [--median] [--std] [--missing txt] [--nvalid]
        RowStatistics.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin and output results(with title) to stdout.
            The first elements as row_name/category_name.
        2. NA as missing value.

    Options:
        -c            Run in category model, group successive rows with the same name together.
        --nvalid      The number of nvalid number for computing summaries.
        --mean        List the mean value.
        --median      List the median value.
        --std         List the standard deviation.
        --min int     List the 'int' number of distinct minimal values.
        --max int     List the 'int' number of distinct maximum values.
        --set int     Output the value set, list the maxium of 'int' values, 0 for listing all.
        --missing txt Set missing values as txt, eg. -1,-2,N. Case sensitive. NA allways as missing.

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
# Input file format(stdin), first column as category name
------------------------
N1      1       2       3
N2      1       NA      4
N2      1       NA      5
N3      a       b       c

# ouput:
# cat test.txt | python3 ./RowStatistics.py --set 10 --min 2 --max 2 --mean --median --std --nvalid
------------------------
NAME    N_VALID MEAN    MEDIAN  STD     MIN_2   MAX_2   SET_10
N1      3       2.0000e+00      2.0000e+00      8.1650e-01      1.0,2.0 2.0,3.0 1,2,3
N2      2       2.5000e+00      2.5000e+00      1.5000e+00      1.0,4.0 1.0,4.0 1,4
N2      2       3.0000e+00      3.0000e+00      2.0000e+00      1.0,5.0 1.0,5.0 1,5
N3      0       NA      NA      NA      NA      NA      b,c,a
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='2.0')

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    TITLE = ['NAME']
    COMBINE_CATEGORY = True if args['-c'] else False
    NUM_MIN = 0
    NUM_MAX = 0
    NUM_SET = 0
    MISSING = set(['NA'])
    if args['--nvalid']:
        TITLE.append('N_VALID')
    if args['--mean']:
        TITLE.append('MEAN')
    if args['--median']:
        TITLE.append('MEDIAN')
    if args['--std']:
        TITLE.append('STD')
    if args['--min']:
        NUM_MIN = int(args['--min'])
        TITLE.append('MIN_%d'%(NUM_MIN))
    if args['--max']:
        NUM_MAX = int(args['--max'])
        TITLE.append('MAX_%d'%(NUM_MAX))
    if args['--set']:
        NUM_SET = int(args['--set'])
        TITLE.append('SET_%d'%(NUM_SET))
    if args['--missing']:
        [MISSING.add(x) for x in args['--missing'].split(',')]

    sys.stdout.write('%s\n'%('\t'.join(TITLE)))
    import numpy
    def processOne(ss_array):
        '''Deal with one value set'''
        #flaten array.
        array = ss_array[0]
        for x in ss_array[1:]:
            array += x[1:]

        out = [array[0]]
        array = [x for x in array[1:] if x not in MISSING] #skip the first element as name.
        float_array = []
        convert_error = False
        for x in array:
            try:
                y = float(x)
                float_array.append(y)
            except Exception as ValueError:
                convert_error = True
        # print(array)
        # print(float_array)
        # print(convert_error)

        if convert_error or len(float_array) == 0:
            if args['--nvalid']:
                out.append('0')
            if args['--mean']:
                out.append('NA')
            if args['--median']:
                out.append('NA')
            if args['--std']:
                out.append('NA')
            if args['--min']:
                out.append('NA')
            if args['--max']:
                out.append('NA')
            if args['--set']:
                ss = list(set(array))
                if NUM_SET >0:
                    ss = ss[:NUM_SET]
                out.append('%s'%(','.join(ss)))
        else:
            if NUM_MAX>0 or NUM_MIN>0:
                distinct_sort = sorted(list(set(float_array)))

            if args['--nvalid']:
                out.append('%d'%(len(float_array)))
            if args['--mean']:
                out.append('%.4e'%(numpy.mean(float_array)))
            if args['--median']:
                out.append('%.4e'%(numpy.median(float_array)))
            if args['--std']:
                out.append('%.4e'%(numpy.std(float_array)))
            if args['--min']:
                ss = distinct_sort[:NUM_MIN]
                out.append('%s'%(','.join(map(str,ss))))
            if args['--max']:
                n = max(0,len(distinct_sort) - NUM_MAX)
                ss = distinct_sort[n:]
                out.append('%s'%(','.join(map(str,ss))))
            if args['--set']:
                ss = list(set(array))
                if NUM_SET >0:
                    ss = ss[:NUM_SET]
                out.append('%s'%(','.join(ss)))

        #output results
        sys.stdout.write('%s\n'%('\t'.join(out)))

    data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if COMBINE_CATEGORY:
                if data:
                    if data[-1][0] == ss[0]:
                        data.append(ss)
                    else:
                        processOne(data)
                        data = []
                        data.append(ss)
                else:
                    data.append(ss)
            else:
                processOne([ss])

    # check the last one if have.
    if data:
        processOne(data)

    # sys.stdout.write('%s\n'%('\n'.join(out_a)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
