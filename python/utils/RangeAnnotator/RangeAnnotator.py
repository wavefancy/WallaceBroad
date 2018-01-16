#!/usr/bin/env python3

"""

    Annotate point value by range categroy.
    @Author: wavefancy@gmail.com

    Usage:
        RangeAnnotator.py -p int -a file [-g int] [-n string]
        RangeAnnotator.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. ***Add one column for the annotion***
        3. See example by -f.

    Options:
        -p int        Column index for position in stdin.
        -g int        The column index for group name in stdin.
                        If this option is on, check the annotion within each group.
        -a file       Range annotation file.
                        If -g is off, three columns: range_start, end, annotion_name
                        If -g is on,   four columns: group name, start, end, annotion_name.
        -n string     Title name for the annotation.
                        Add this string for those lines can be parsed
                        as float in the position column. Default: ANN.
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
#stdin:
------------------------
1	2
2	4
1	3
3	1

# ann.1.txt
------------------------
1	2	a1
3	3	a2

#output: -p 2 -a ann.1.txt -n txt
------------------------
1       2       a1
2       4       txt
1       3       a2
3       1       a1

# ann.2.txt
------------------------
1	1	2	a1
1	2	3	a2
2	1	5	a3

#output: -p 2 -a ann.2.txt -g 1 -n txt
------------------------
1       2       a1,a2
2       4       a3
1       3       a2
3       1       txt
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    pcol = int(args['-p'])-1
    gcol = int(args['-g'])-1 if args['-g'] else -1
    aname = args['-n'] if args['-n'] else 'ANN'
    afile = args['-a']

    #read annotion file.
    grangemap = {} #group name -> [(start,end,name),...]
    with open(afile,'r') as afileinput:
        for line in afileinput:
            line = line.strip()
            if line:
                ss = line.split()
                gname = 'g'
                if gcol >= 0:
                    gname = ss[0]
                    ss = ss[1:]
                if gname not in grangemap:
                    grangemap[gname] = []

                grangemap[gname].append((float(ss[0]), float(ss[1]), ss[2]))

    # print(grangemap)
    def getAnno(gname, pos):
        '''Check the annotation for specific point'''
        # print(':::' + str(gname) + '---' + str(pos))
        re = []
        if gname in grangemap:
            for s,e,n in grangemap[gname]:
                if pos>=s and pos <= e:
                    re.append(n)
        return re

    gname = 'g'
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if gcol >= 0:
                gname = ss[gcol]

            try:
                pos = float(ss[pcol])
                re = getAnno(gname,pos)
                if re:
                    ss.append(','.join(re))
                else:
                    ss.append(aname)
            except Exception as e:
                ss.append(aname)

            sys.stdout.write('%s\n'%('\t'.join(ss)))
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
