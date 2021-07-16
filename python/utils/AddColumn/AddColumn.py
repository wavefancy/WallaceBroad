#!/usr/bin/env python3

'''

    Add one or more columns.

    @Author: wavefancy@gmail.com, Wallace Wang.

    Usage:
        AddColumn.py (-c int|-l) (-v text | -i int | -e ints | -w file) [-t txt] [-d text]
        AddColumn.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.

    Options:
        -c int        After which column(int, 1 based) from the input for insertting new column.
                        0 for add column at the line begining.
        -l            Add extra column to the last of a line.
        -t text       The title for the new inserting column(s).
                eg. t1|t1,t2. Split values by ','. len(-t) == len(-v).
        -i int        Add index value for each row, index start from 'int'.
        -v text       The value for the new inserting column(s).
                        eg. v1|v1,v2. v1,v2 add two columns, split values by ','
        -e ints       Using the Existing columns as the content for the new column.
                        eg. 1|1,3. ints for the column index, based on input file, 1 based.
                        Copied columns were concatenated by ':'.
        -w file       Mix columns as a new column according to mixture weight.
                        Each line of two fields: column_title, weight.
        -d text       Set up the field delimiter, default tab.
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
1       2
1       2

cat test.txt | python3 AddColumn.py -c 1 -v 0,0 -t t1,t2
------------------------
1       t1      t2      2
1       0       0       2

cat test.txt | python3 AddColumn.py -c 1 -i 3
1       3       2
1       4       2

cat test.txt | python3 AddColumn.py -c 0 -e 1,2 -t T
T       1       2
1:2     1       2
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    COL     = int(args['-c']) if args['-c'] else None
    LAST    = True if args['-l'] else False
    DELIMITER = args['-d'] if args['-d'] else '\t'

    # Option swith to turn on different functions.
    COPY_VALS = [int(x)-1 for x in args['-e'].split(',')] if args['-e'] else None #merge columns as a new column.
    VALS      = args['-v'].split(',') if args['-v'] else None # add constant values.
    INDEXV    = int(args['-i'])       if args['-i'] else None # add index value.
    
    WEIGHTs     = {} # merge columns as a new column by according weight. mappig name to weight.
    WEIGHT_COLS = []
    INDEXMAP = {} # mapping name to column index.
    WeightTitleLine = False
    # loading weight from file.
    if args['-w']:
        WeightTitleLine = True
        with open(args['-w'],'r') as reader:
            for line in reader:
                line = line.strip()
                if line:
                    ss = line.split()
                    if ss[0] in WEIGHTs:
                        sys.stderr.write('ERROR: duplicate key in -w weight file, key:%s \n'%(ss[0]))
                    else:
                        WEIGHTs[ss[0]] = float(ss[1])


    TITLES  = args['-t'].split(',') if args['-t'] else VALS
    

    if VALS and len(VALS) != len(TITLES):
        sys.stderr.write('ERROR: the element length for -t and -v should be the same!\n')
        sys.exit(-1)


    for line in sys.stdin:
        line = line.strip()
        if line :
            ss = line.split(DELIMITER)
            if LAST:
                COL = len(ss)
                LAST = False

            # deal with the title line, find out the index for the column defined in weight file.
            if WeightTitleLine:
                for k,v in zip(ss, range(len(ss))):
                    if k in INDEXMAP:
                        sys.stderr.write('ERROR, Dupliciate values in title, -t model failed! DUP KEY: %s\n'%(k))
                        sys.exit(-1)
                    else:
                        INDEXMAP[k] = v
                for k in WEIGHTs.keys():
                    if k not in INDEXMAP:
                        sys.stderr.write('ERROR, key not in title: %s\n'%(k))
                        sys.exit(-1)
                    else:
                        WEIGHT_COLS.append(INDEXMAP[k])
                WeightTitleLine = False

            out = ss[:COL]
            # print(ss)
            if TITLES:
                out = out + TITLES + ss[COL:]
                TITLES = None
            else:
                # Add a fix value to a new column.
                if VALS:
                    out = out + VALS + ss[COL:]
                # Add line index as a new column. start_int, start_int +1, start_int+2 ... start_int+n
                elif INDEXV:
                    out = out + [str(INDEXV)] + ss[COL:]
                    INDEXV += 1
                # Comine a few existed column together as a new column.
                elif COPY_VALS:
                    # print('Here!')
                    temp = [ss[x] for x in COPY_VALS]
                    out = out + [':'.join(temp)] + ss[COL:]
                # Mixture columns by weight.
                elif WEIGHTs:
                    val = 0
                    for k,i in zip(WEIGHTs.keys(), WEIGHT_COLS):
                        val += WEIGHTs[k] * float(ss[i])
                    out = out + ['%g'%(val)] + ss[COL:]
                else:
                    sys.stderr.write('ERROR: please set proper parameters!\n')
                    sys.exit(-1)

            sys.stdout.write('%s\n'%(DELIMITER.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
