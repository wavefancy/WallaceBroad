#!/usr/bin/env python3

"""

    x = (x-mean(x))/sd(x)

    @Author: wavefancy@gmail.com

    Usage:
        NormalStandardizer.py -c col [(-m mean -s sd) | --mz]
        NormalStandardizer.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output to stdout.
        2. Add one column for normalized value.
        3. Column index start from 1.

    Options:
        -c col        Column index|name for value to be normalized.
        -m mean       Specify mean, use this value other than estimated from data.
        -s sd         Specify sd, use this value other than estimated from data.
        --mz          Shift the the minimal value to 0. [x-min(x) for x in standardizedValues]
                          This option can not be used with -m and -s.
        -h --help     Show this screen.
        -v --version  Show version.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

class P(object):
    col = 0
    mean = -1
    sd = -1

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    WITH_TITLE = False
    P.col = -1
    try: 
        P.col = int(args['-c']) -1
    except:
        WITH_TITLE = True
    
    if args['--mz'] and args['-m']:
        sys.stderr.write('ERROR: --mz can not be used with -m.\n')

    INDEXMAP = {}
    if args['-m']:
        P.mean = float(args['-m'])
        P.sd = float(args['-s'])
        for line in sys.stdin:
            line = line.strip()
            if line:
                if WITH_TITLE:
                    ss = line.split()
                    for k,v in zip(ss, range(len(ss))):
                        if k in INDEXMAP:
                            sys.stderr.write('ERROR, Dupliciate values in title, can not use column name. DUP KEY: %s\n'%(k))
                            sys.exit(-1)
                        else:
                            INDEXMAP[k] = v
                    if args['-c'] in INDEXMAP:
                        P.col = INDEXMAP[args['-c']]
                    else:
                        sys.stderr.write('ERROR, name "%s" not in title!'%(args['-c']))
                        sys.exit(-1)
                    # Output title
                    sys.stdout.write('%s\tNormedValue\n'%(line))
                    WITH_TITLE = False

                else:
                    try:
                        ss = line.split()
                        vv = float(ss[P.col])

                        sys.stdout.write('%s\t%.4e\n'%(line, (vv - P.mean)/P.sd))

                    except ValueError:
                        sys.stderr.write('Warning: parse value error at line (skiped): %s\n'%(line))

    else:
        content = [] # [(line, val),...]
        for line in sys.stdin:
            line = line.strip()
            if line:
                if WITH_TITLE:
                    ss = line.split()
                    for k,v in zip(ss, range(len(ss))):
                        if k in INDEXMAP:
                            sys.stderr.write('ERROR, Dupliciate values in title, can not use column name. DUP KEY: %s\n'%(k))
                            sys.exit(-1)
                        else:
                            INDEXMAP[k] = v
                    if args['-c'] in INDEXMAP:
                        P.col = INDEXMAP[args['-c']]
                    else:
                        sys.stderr.write('ERROR, name "%s" not in title!'%(args['-c']))
                        sys.exit(-1)
                    # Output title
                    sys.stdout.write('%s\tNormedValue\n'%(line))
                    WITH_TITLE = False
                else:
                    try:
                        ss = line.split()
                        vv = float(ss[P.col])

                        content.append([line, vv])
                    except ValueError:
                        sys.stderr.write('Warning: parse value error at line (skiped): %s\n'%(line))

        vals = [x[1] for x in content]

        import numpy
        mm = numpy.mean(vals)
        sd = numpy.std(vals)

        #Normalize
        for x in content:
            x[1] = (x[1]-mm)/sd

        if args['--mz']:
            minv = min([x[1] for x in content])
            for x in content:
                x[1] = x[1] - minv

        for line, vv in content:
            sys.stdout.write('%s\t%.6f\n'%(line, vv))


sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
