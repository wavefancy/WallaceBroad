#!/usr/bin/env python3

'''

    Plot heatmap of data matrix.

    @Author: wavefancy@gmail.com, Wallace Wang.

    Usage:
        HeatmapCluster.py -o filename -s size [--color cname --std int --nxlabel --nylabel --rc file]
        HeatmapCluster.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.

    Options:
        -o filename   Output filename, eg: output.pdf.
        -s size       Set figure size, width,height, two number.
        --color cname Set color scheme name, default: YlGnBu.
                          Check the cmap keyword from ref2.
        --std int     Set row(0) or column(1) based z-score normalize. (x-E(x))/sd(x)
                        0|1, or do not set this option.
        --nxlabel     Do not show xlabel.
        --nylabel     Do not show ylabel.
        --rc file     Color rows, one column for color.
        -h --help        Show this screen.
        --version     Show version.
        -f --format   Show input/output file format example.

    REF:
        1. https://seaborn.pydata.org/generated/seaborn.clustermap.html
        2. https://seaborn.pydata.org/generated/seaborn.heatmap.html

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.
from docopt import docopt

def ShowFormat():
    '''File format example'''
    print('''
#Input file data matrix with column and row name.
------------------------
Sample  T1      T2      T3
ID1     1       2       3
ID2     4       5       1
ID3     7       3       1
ID4     2       1       4
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    sys.stdout.write(str(args)+'\n')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    import matplotlib as mpl
    mpl.use('Agg')
    import pandas as pd
    import seaborn as sns;
    sns.set(color_codes=True)

    OUTPUTFILE = args['-o']
    ss         = args['-s'].split(',')
    WIDTH      = float(ss[0])
    HEIGHT     = float(ss[1])
    CMAP       = args['--color'] if args['--color'] else 'YlGnBu'
    STD        = None
    xticklabels = False if args['--nxlabel'] else True
    yticklabels = False if args['--nylabel'] else True
    if args['--std']:
        STD = int(args['--std'])
    row_colors = None
    if args['--rc']:
        row_colors = pd.read_table(args['--rc'],header=0,delim_whitespace=True)

    data = pd.read_table(sys.stdin,header=0,delim_whitespace=True,index_col=0)
    # print(data)
    # print(row_colors)
    g = sns.clustermap(data.reset_index(drop=True),
        cmap=CMAP,
        metric="correlation",
        # standard_scale=1,
        z_score=STD,
        xticklabels=xticklabels,
        yticklabels=yticklabels,
        row_colors = row_colors,
        figsize=(WIDTH, HEIGHT))
    g.savefig(OUTPUTFILE)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
