#!/usr/bin/env python3

"""

    Qsub helper for The Univa Grid Engine (UGE) at Broad.
    @Author: wavefancy@gmail.com

    Usage:
        qsubHelper.py [-t int] [-m int] [-c int] [-n string] [-f] [--os name]
        qsubHelper.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read command line from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -t int        Set the running hours for the jobs, default 2.
        -c int        Set the number of cpu cores, default 2.
        -m txt        Set the memory size, default 2G. Default unit is G.
                         Specify in MB by like 100M.
                         The actual memory loaded is [-c] * [-m], also depending
                         on the number of cpus requested.
        -n string     Set job name, default 'name'.
        --os name     Set up the os class name, default no set, eg. RedHat7
        -f            Put commands to files and return the commands for run from file.
        -h --help     Show this screen.
        -v --version  Show version.
        --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
# Input
------------------------
line1
line2

#output: -t 10 -m 5 -c 3 -n test
------------------------
qsub -cwd -j y -l h_rt=10:0:0 -l h_vmem=5g -pe smp 3 -binding linear:3 -N test_1 -b y 'line1'
qsub -cwd -j y -l h_rt=10:0:0 -l h_vmem=5g -pe smp 3 -binding linear:3 -N test_2 -b y 'line2'
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.2')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    N_CPU  = args['-c'] if args['-c'] else '2'
    N_MEM  = args['-m'] if args['-m'] else '2G'
    if N_MEM[-1].isdigit():
        N_MEM += 'G'
    N_HOUR = args['-t'] if args['-t'] else '2'
    N_NAME = args['-n'] if args['-n'] else 'name'

    # additional options we will add in.
    addition = ''
    if args['--os']:
        addition += ('-l os=' + args['--os'])

    temp = 0
    for line in sys.stdin:
        line = line.strip()
        if line:
            temp += 1
            #sys.stdout.write("qsub -cwd -l h_rt=%s:0:0 -l h_vmem=%sg -pe smp %s -binding linear:%s -q %s -b y bash -c '%s'\n"
            if args['-f']:
                fn = "%s_%d.bash"%(N_NAME, temp)
                with open(fn,'w') as ofile:
                    ofile.write('%s\n'%(line))

                out = 'qsub -cwd -j y -l h_rt=%s:0:0 -l h_vmem=%s -pe smp %s -binding linear:%s -N %s_%d %s -b y "%s"\n'%(N_HOUR,N_MEM,N_CPU,N_CPU,N_NAME,temp,addition,"bash ./"+fn)

            else:
                out = 'qsub -cwd -j y -l h_rt=%s:0:0 -l h_vmem=%s -pe smp %s -binding linear:%s -N %s_%d %s -b y "%s"\n'%(N_HOUR,N_MEM,N_CPU,N_CPU,N_NAME,temp,addition,line)

            sys.stdout.write(out)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
