#!/usr/bin/env python3

"""

    Scatter plot by Altair, output vega-lite json to stdout.
    @Author: wavefancy@gmail.com

    Usage:
        AScatter.py -x text -y text [-c text] [-s text] [-H height] [-W width] [--abline text]
        AScatter.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data with header from stdin, and save figure to file.
        2. Default delimiter is '\s+'.

    Options:
        -x text       Column name for X data.
        -y text       Column name for Y data.
        -c text       Column name for set color.
        -s text       Column name for set mark size.
        -H height     Figure height, int, default 300.
        -W width      Figure width, int, default 400.
        --abline text Make abline, x1_y2_x2_y2.

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

    import altair as alt
    from vega_datasets import data
    import pandas as pd

    x = args['-x']
    y = args['-y']
    # outname = args['-o']
    color = args['-c'] if args['-c'] else None
    size  = args['-s'] if args['-s'] else None
    fheight = int(args['-H']) if args['-H'] else 300
    fwidth  = int(args['-W']) if args['-W'] else 400
    abline = pd.DataFrame()
    if args['--abline']:
        temp = [float(x) for x in args['--abline'].split('_')]
        abline_x = []; abline_y = []
        abline_x.append(temp[0]);abline_x.append(temp[2])
        abline_y.append(temp[1]);abline_y.append(temp[3])
        abline['x'] = abline_x
        abline['y'] = abline_y


    # make altair can handle large files.
    # https://altair-viz.github.io/user_guide/faq.html
    alt.data_transformers.enable('default', max_rows=None)

    # iris = data.iris()
    data = pd.read_csv(sys.stdin, header=0, delimiter='\s+')

    def urban_theme():
        # Axes
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
                "config": {
                    "axisX": {
                        "domain": True,
                        "domainColor": axisColor,
                        "domainWidth": 2,
                        # "grid": False,
                        # "labelFont": labelFont,
                        "labelFontSize": 12,
                        "tickColor": axisColor,
                        "tickSize": 5, # default, including it just to show you can change it
                        "tickWidth": 2,
                        # "titleFont": font,
                        "titleFontSize": 12,
                        # "titlePadding": 10, # guessing, not specified in styleguide
                        # "title": "X Axis Title (units)",
                    },
                    "axisY": {
                        "domain": True,
                        "grid": True,
                        "domainColor": axisColor,
                        "domainWidth": 2,
                        "gridColor": gridColor,
                        "gridWidth": 1,
                        # "labelFont": labelFont,
                        "labelFontSize": 12,
                        # "labelAngle": 0,
                        # "ticks": False, # even if you don't have a "domain" you need to turn these off.
                        # "titleFont": font,
                        "tickColor": axisColor,
                        "tickWidth": 2,
                        "titleFontSize": 12,
                        # "titlePadding": 10, # guessing, not specified in styleguide
                        # "title": "Y Axis Title (units)",
                        # titles are by default vertical left of axis so we need to hack this
                        # "titleAngle": 0, # horizontal
                        # "titleY": -10, # move it up
                        # "titleX": 18, # move it to the right so it aligns with the labels
                    },
                    }
            }
    # https://towardsdatascience.com/consistently-beautiful-visualizations-with-altair-themes-c7f9f889602
    alt.themes.register("my_custom_theme", urban_theme)
    alt.themes.enable("my_custom_theme")

    # we explictly set the titles for x and y axis, this will hidden the titles from abline later on.
    # https://altair-viz.github.io/user_guide/generated/core/altair.Axis.html
    # alt.Axis(grid=False)
    paras = dict(
        x=alt.X(x,title=x),
        y=alt.Y(y,title=y))
    if color:
        paras['color'] = color
    if size:
        paras['size'] = size


    out_plot = alt.Chart(data).mark_point().encode(**paras)

    if not abline.empty:
        a = alt.Chart(abline).mark_line(strokeDash=[8,2],color='red').encode(x='x',y='y')
        out_plot += a

    # chart.save(outname, webdriver='firefox')
    # chart.save(outname, vega_version='4')
    # make configure_view here, as we finished all plot.
    out_plot.configure_view(
            height = fheight,
            width  = fwidth
        )
    print(out_plot.to_json())

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
