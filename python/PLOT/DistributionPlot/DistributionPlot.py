#!/usr/bin/env python3

"""

    Plot distribution data by plotly.
    @Author: wavefancy@gmail.com

    Usage:
        DistributionPlotV2.py -o outname -x xtitle [-t] [--bs binsize] [--an anno] [--xr xrange] [--yr yrange] [--xdt xdtick] [--ydt ydtick] [--nc] [-l] [-p] [--lm int] [--rm int] [--tm int] [--cl text] [--title txt] [--hhist] [--sy] [--nyg] [--cn] [--vl vline] [--hl hline] [-d txt]
        DistributionPlotV2.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -x xtitle
        -t            In test mode.
        -o outname    Output file name: output.html.
        -d txt        Set delimter for split column, default whitesapces. tab for '\\t'.
        --bs binsize  Set binsize, float, default 0.2
        -l            Show legned, default False.
        --an anno     Vertical arrow annotation, pattern as: x_y_text_color[_arrowLen],x_y_text_color...
                      [_arrowLen] is optional, default 100.
        --xdt float   Distance between x ticks.
        --ydt float   Distance between y ticks.
        --yerr yecol  Column index for y error bar.
        --xr xrange   Set the xAxis plot range: float1,float2.
        --yr yrange   Set the yAxis plot range: float1,float2,
                      *** Please set this parameter to fix the bug of two horizontal lines for xAxis.
        --nyg         Do not show grid lines for y axis, default show.
        --sy          Show Y Axis, default no show.
        --nc          Do not display fitting curve.
        --cn          Fit curve by 'normal' model, default kde.
        --hhist       Do not display histnorm bar, default show.
        --hl hline    Add horizontal lines: float1,float2.
        --vl vline    Add vertical lines: float1, float2...
        --ms msize    Set marker size: float, default 5.
        -p            Set histnorm as 'probability', default: 'probability density'
        --lm int      Set left margin, default 50.
        --rm int      Set right margin, default 30.
        --tm int      Set top margin, default 30.
        --cl text     Set color for distribution, eg '#37AA9C|#37AA9C::red'
        --title txt   Set the title of the plot figure.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

        https://plot.ly/python/distplot/
        https://plot.ly/python/text-and-annotations/
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    #input example
    ------------------------
c1  1
c1  2
c1  5
c2  2
c2  10
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='2.1')
    #verison 2.0
    # 1. add function to change bin_size
    # 2. add function to add arrow annotation.

    #version 2.1
    # 1. add function to change arrow length for annotation.

    print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    errYCol = '' #value column for error bar for Y.
    xtitle = args['-x']
    #ytitle = args['-y']
    ytitle = 'Density'
    outname = args['-o']
    mode = 'markers'
    hlines = [] #location for horizontal lines.
    vlines = []
    ablines = []
    msize = 5
    binsize = 0.2
    lm = 50 #left margin
    rm = 30 #right margin
    tm = 30 #top margin
    figureTitle = ''
    yGRID = False if args['--nyg'] else True
    delimter = args['-d'] if args['-d'] else ''
    if delimter == 'tab':
        delimter = '\t'

    if args['--bs']:
        binsize = float(args['--bs'])
    arowAnnotation = ''
    if args['--an']:
        arowAnnotation = args['--an']
    xdt = ''
    if args['--xdt']:
        xdt = float(args['--xdt'])
    ydt = ''
    if args['--ydt']:
        ydt = float(args['--ydt'])

    xrange = None
    if args['--xr']:
        xrange = list(map(float, args['--xr'].split(',')))
    yrange = None
    if args['--yr']:
        yrange = list(map(float, args['--yr'].split(',')))
    if args['--lm']:
        lm = int(args['--lm'])
    if args['--rm']:
        rm = int(args['--rm'])
    if args['--tm']:
        tm = int(args['--tm'])
    show_curve = True
    if args['--nc']:
        show_curve = False
    showlegend = False
    if args['-l']:
        showlegend = True
    histnorm = 'probability density'
    if args['-p']:
        histnorm = 'probability'
        ytitle = 'Probability'
    colors = ['#37AA9C', '#E26868','#FFA556','#2BCDC1','#F66095','#393E46']
    if args['--cl']:
        colors = args['--cl'].split('::')
    if args['--title']:
        figureTitle = args['--title']
    show_hist = False if args['--hhist'] else True
    CTYPE     = 'normal' if args['--cn'] else 'kde'

    if args['--hl']:
        hlines = list(map(float, args['--hl'].split(',')))
    if args['--vl']:
        vlines = list(map(float, args['--vl'].split(',')))

    # Show Y axis or not.
    yAxisShow = False
    yTickWay  = ''
    if args['--sy']:
        yAxisShow = True; yTickWay = 'outside'

    commands = {'vl'}
    data = [] #[[name, val1,val2 ..], [name, val1, val2...]]

    from collections import OrderedDict
    dataMap = OrderedDict() # name -> values.
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split(delimter)
            if ss[0]=='COMMAND' and ss[1] in commands:
                if ss[1] == 'vl':
                    vlines.append(float(ss[2]))
            else:
                if ss[0] not in dataMap:
                    dataMap[ss[0]] = []
                else:
                    dataMap[ss[0]].append(float(ss[1]))

    import plotly
    import plotly.plotly as py
    import plotly.graph_objs as go
    from plotly import figure_factory as FF

    if args['-t']:
        import numpy as np
        dataMap = {'test': np.random.randn(400)}

    hist_data = []
    group_labels = []
    for k,v in dataMap.items():
        hist_data.append(v)
        group_labels.append(k)

    # Create distplot
    # https://plot.ly/python/distplot/
    fig = FF.create_distplot(hist_data, group_labels,bin_size=binsize,
        histnorm=histnorm,
        curve_type=CTYPE,
        colors=colors,
        show_curve= show_curve,
        show_hist=show_hist,
        show_rug=False)

    afsize = 10 #annotation font size.
    #arrow annotation
    annoArray = []
    if arowAnnotation:
        for x in arowAnnotation.split(','):
            ss = x.split('_')
            arrowLen = -100
            if len(ss) == 5:
                arrowLen = -1 * int(ss[4])

            annoArray.append(
                dict(
                    x=float(ss[0]),
                    y=float(ss[1]),
                    xref='x',
                    yref='y',
                    #yref='paper',
                    text=ss[2],
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor=ss[3],
                    font=dict(
                        color=ss[3],
                        size = afsize,
                    ),
                    ax=0,
                    ay=arrowLen
                ))

    annoLayout = go.Layout(
        annotations = annoArray
    )

    layout = go.Layout(
        titlefont=dict(
            size=14
        ),
        # change global font color to black.
        # https://plot.ly/python/font/
        font=dict(color='black'),
        #title='Points Scored by the Top 9 Scoring NBA Players in 2012',
        yaxis=dict(
            title=ytitle,
            dtick = ydt,
            range=yrange,
            # ticks='outside',
            ticks=yTickWay,
            showline=yAxisShow,
            showgrid=yGRID,
            color='black'
        #     zeroline=False,
        #     #dtick=5,
            #white grid line
            # gridcolor='rgb(255, 255, 255)',
        #     #gridwidth=1,
        #     zerolinecolor='rgb(255, 255, 255)',
        #     zerolinewidth=2,
        ),
        xaxis=dict(
            title = xtitle,
            range=xrange,
            dtick = xdt,
            ticks='outside',
            showline=True,
            # Sets default for all colors associated with this axis
            color='black'
        )
        ,
        margin=dict(
            l=lm,
            r=rm,
            b=40,
            t=tm,
        ),
        # paper_bgcolor='rgb(243, 243, 243)',
        # plot_bgcolor='rgb(243, 243, 243)',
        showlegend=showlegend
    )

    fig['layout'].update(layout)
    if annoArray:
        fig['layout'].update(annoLayout)
    if figureTitle:
        fig['layout'].update(go.Layout(title=figureTitle))
    #fig = go.Figure(data=traces, layout=layout)
    #py.iplot(fig)
    #output the last one

    # add lines annotation.
    hl_data = []
    if hlines:
        for y in hlines:
            hl_data.append(
                {
                    'type': 'line',
                    'xref': 'paper',
                    'x0': 0,
                    'y0': y,
                    'x1': 1,
                    'y1': y,
                    'line': {
                        #'color': 'rgb(50, 171, 96)',
                        #'color': '#E2E2E2',
                        'color': 'rgba(0, 0, 0, 0.5)',
                        'width': 1,
                        # 'dash': 'dashdot',
                        # ['solid', 'dot', 'dash', 'longdash', 'dashdot','longdashdot']
                        'dash': 'dot',
                }}
            )
        #h = {'shapes':hl_data}
        #layout.update(h)

    #add for ablines
    ab_data = []
    if ablines:
        for y in ablines:
            #print(y)
            cc = abcolor
            if len(y) == 5:
                cc = y[4]

            # set the layer of elements.
            # https://github.com/plotly/plotly.js/issues/923
            ab_data.append(
                {
                    'type': 'line',
                    # 'xref': 'paper',
                    'x0': y[0],
                    'y0': y[1],
                    'x1': y[2],
                    'y1': y[3],
                    'layer': 'below',
                    'line': {
                        'color': cc,
                        #'color': 'rgba(0, 0, 0, 0.5)',
                        'width': 2,
                        'dash': 'dashdot'
                    }
                }
            )

    # https://plot.ly/python/reference/#layout-shapes-items-shape-layer
    vl_data = []
    if vlines:
        for y in vlines:
            vl_data.append(
                {
                    'type': 'line',
                    'yref': 'paper',
                    # default above.
                    'layer': 'below',
                    'x0': y,
                    'y0': 0,
                    'x1': y,
                    'y1': 1,
                    'line': {
                        # 'color': '#FFD979',
                        'color': 'rgba(0, 0, 0, 0.5)',
                        'width': 2,
                        # 'dash': 'dashdot',
                        'dash': 'dot',
                }}
            )
        #h = {'shapes':vl_data}
        #layout.update(h)
    # print(vlines)
    alllines = hl_data + vl_data + ab_data
    if alllines:
        h = {'shapes':alllines}
        # layout.update(h)
        fig['layout'].update(h)

    plotly.offline.plot(fig
         ,show_link=False
         ,auto_open=False
         ,filename=outname
    )
    #fig = go.Figure(data=plotData, layout=layOut)
    #py.image.save_as(fig,outname,width='10in',height='3in')
    #py.image.save_as(fig,outname,width=700,height=500)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
