#!/usr/bin/env python3

"""

    Scatter plot by seaborn.

    @Author: wavefancy@gmail.com

    Usage:
        SeaCatterPlot.py -o txt [-x txt] [-y txt] [--col txt] [--ncol int] [--hue txt]
                        [--context txt] [--legend int]
        SeaCatterPlot.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin as dataframe.
        2. See example by -f.

    Options:
        -x txt        Colum name for x, default x.
        -y txt        Colum name for y, default y.
        -o txt        Output file name.
        --col txt     Plot data in subfigure, group data by txt.
        --ncol int    Array subfigure in int columns, default None.
        --hue txt     Colum name for color.
        --context txt Set plot context,talk|paper|poster|notebook, default talk.
        --legend int  Set the location of legend, 0 for hidden, default as 0.
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
#in each chromosome, pos should be sorted.
------------------------
chr,xx,yy
chr1,100,10
chr1,200,5
chr1,300,2
chr2,300,5
chr2,500,15

#output:
------------------------

    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='2.2')
    # version 2.2: add the option for abline.
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    import seaborn as sns
    import pandas as pd
    xname    = args['-x'] if args['-x'] else 'x'
    yname    = args['-y'] if args['-y'] else 'y'
    colname  = args['--col'] if args['--col'] else None
    ncol     = int(args['--ncol']) if args['--ncol'] else None
    hue      = args['--hue'] if args['--hue'] else None
    out      = args['-o']
    context  = args['--context'] if args['--context'] else 'talk'
    legend   = args['--legend'] if args['--legend'] else '0'

    #load data from stdin
    data = pd.read_csv(sys.stdin,header=0,delimiter=',')
    # print(data)
    # print(type(data))

    sns.set_context(context)
    sns.set_style("ticks",{
        'axes.grid': True,
        'grid.color': '0.8', # the larger the value the lighter.
        'grid.linestyle': ':'
     })
    # print(ncol)
    g = sns.scatterplot(x=xname, y=yname,
            hue=hue,
            # col = colname,
            # col_wrap = ncol,
            data=data)

    figure = g.get_figure()
    figure.savefig(out)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
