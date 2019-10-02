#!/usr/bin/env python3

"""

    Generate table one according to input data.

    @Author: wavefancy@gmail.com

    Usage:
        Tableone.py [-c txt] [-g txt] [-n txt] [-f filename] [--fmt txt]
        Tableone.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read cvs data from stdin, and output results to stdout.
        2. Line starts with '#' will be copy to stdout directly, useful for title.
        3. Count the number of algorithms with damaging predction, and output the
            records meet the threshold (>=).

    Options:
        -c text       Column names for categorical variable, eg. title1,title2.
        -g text       Column name  for categorical variable stratification, 
                        usually the case/control status.
        -n text       Column names for non-normal variables.
        -f filename   Copy results to file, output format specified by '--fmt'
        --fmt  txt    Output file format, csv|latex|html, default csv.
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
#input:
# https://raw.githubusercontent.com/tompollard/tableone/master/data/pn2012_demo.csv
#-------------------
# cat pn2012_demo.csv | python3 Tableone.py -c ICU,death -n Age,LOS -f out.csv -g death

# cat pn2012_demo.csv | python3 Tableone.py -c ICU,death -n Age,LOS -f out.csv
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    categorical  = args['-c'].split(',') if args['-c'] else None
    nonnormal    = args['-n'].split(',') if args['-n'] else None
    group        = args['-g']    if args['-g']    else None
    pval         = True          if args['-g']    else False
    outfile      = args['-f']    if args['-f']    else None
    outFMT       = args['--fmt'].lower() if args['--fmt'] else 'csv'

    from tableone import TableOne
    import pandas as pd

    data = pd.read_csv(sys.stdin)
    # create grouped_table with p values
    # API: https://tableone.readthedocs.io/en/latest/tableone.html
    # Example: https://github.com/tompollard/tableone/blob/master/tableone.ipynb
    grouped_table = TableOne(data, categorical=categorical, groupby=group, 
        nonnormal=nonnormal, label_suffix=True, pval = pval)
    print(grouped_table)

    if outfile:
        if outFMT == 'csv':
            grouped_table.to_csv(outfile)
        elif outFMT == 'latex':
            grouped_table.to_latex(outfile)
        elif outFMT == 'html':
            grouped_table.to_html(outfile)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
