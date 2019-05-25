#!/usr/bin/env python3

"""

    Scatter plot by Altair, output vega-lite json to stdout.
    @Author: wavefancy@gmail.com

    Usage:
<<<<<<< HEAD
        AScatter.py -x text -y text -o outname [-c text] [-s text]
=======
        AScatter.py -x text -y text [-c text] [-s text]
>>>>>>> 5547cdca9a34d0abd8bbf85e4fe022aaf9db5da5
        AScatter.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data with header from stdin, and save figure to file.
        2. Default delimiter is '\s+'.

    Options:
        -x text       Column name for X data.
        -y text       Column name for Y data.
        -c text       Column name for set color.
        -s text       Column name for set mark size.
<<<<<<< HEAD
        -o outname    Output file name: output.html.
=======
>>>>>>> 5547cdca9a34d0abd8bbf85e4fe022aaf9db5da5

    API:
        https://altair-viz.github.io/getting_started/installation.html
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)
    sys.stderr.write(str(args))

    x = args['-x']
    y = args['-y']
    # outname = args['-o']
    color = args['-c'] if args['-c'] else None
    size  = args['-s'] if args['-s'] else None

    import altair as alt
    from vega_datasets import data
    import pandas as pd

    # iris = data.iris()
    data = pd.read_csv(sys.stdin, header=0, delimiter='\s+')
    # print(data)
    paras = dict(x=x,y=y)
    if color:
        paras['color'] = color
    if size:
        paras['size'] = size

    # chart = alt.Chart(data).mark_point().encode(
    #     x=x,
    #     y=y,
    #     color=color
    # )
    chart = alt.Chart(data).mark_point().encode(**paras)

    # chart.save(outname, webdriver='firefox')
    # chart.save(outname, vega_version='4')
    print(chart.to_json())

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
