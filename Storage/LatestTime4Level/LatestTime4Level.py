#!/usr/bin/env python3

"""

    Convert N lines to a single one line, repeat until file end.

    @Author: wavefancy@gmail.com

    Usage:
        LatestTime4Level.py [-l int]
        LatestTime4Level.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. Input line by line, each line three columns: USERNAME FileSize LastAccessData FileName.
        3. See example by -f.

    Options:
        -l int        The level for grouping files, default 4.
                        /medpop/esp/USERNAME/PROJECTS/....
                        Level1  L2  L3      L4 .... Ln.
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
#input:
------------------------
name1   2       2017-11-07      /medpop/esp2/abick/dbgap/aric/
name1   3       2018-11-07      /medpop/esp2/abick/dbgap/aric/
name2   1       2017-11-07      /medpop/esp2/abick/dbgap/aric/
name3   5       2017-11-07      /medpop/esp2

#output: -n 0
------------------------
name1   2018-11-07      5       /medpop/esp2/abick/dbgap
name2   2017-11-07      1       /medpop/esp2/abick/dbgap
name3   2017-11-07      5       /medpop/esp2

    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    LEVEL = int(args['-l']) if args['-l'] else 4
    LEVEL = LEVEL + 1
    DATEFORMAT = '%Y-%m-%d'

    from collections import OrderedDict
    from datetime import datetime
    groupMap = OrderedDict() #'USERNAME-FileLevelName' -> (TotalSize, LastAccessData)

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split(None,3)
            LevelName = '/'.join(ss[3].split('/',LEVEL)[:LEVEL])
            date = datetime.strptime(ss[2], DATEFORMAT)
            size = int(ss[1])
            key = ss[0] + '-' + LevelName
            if key not in groupMap:
                groupMap[key] = [size, date]
            else:
                groupMap[key][0] += size
                if date > groupMap[key][1]:
                    groupMap[key][1] = date

    #output results.
    for k,v in groupMap.items():
        ss = k.split('-',1)
        sys.stdout.write('%s\t%s\t%d\t%s\n'%(ss[0],v[1].strftime(DATEFORMAT),v[0],ss[1]))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
