#!/usr/bin/env python3

"""

    Plot category data as box plot using plotly library.
    @Author: wavefancy@gmail.com

    Usage:
        BoxPlot.py -y ytitle -o outname [-x xtitle ] [--yerr ycol] [--yr yrange] [--hl hline] [--xls int] [--ylfs int] [--rm int] [--lm int] [--rx int] [--ry int] [--ms msize] [--over] [--bm bmargin] [--ha hanno] [--ady ady] [--haw float] [--hat int] [--cl colors] [--ydt float] [--c2] [--yt txt] [--nobox] [--nooutliers] [--atext txt] [--atr int] [--ngy] [--sy]
        BoxPlot.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -x xtitle
        -y ytitle
        -o outname    Output file name: output.html.
        --yerr yecol  Column index for y error bar.
        --rx int      Set the angle for rotate x label.
        --ry int      Set the angle for rotate y label.
        --xls int     Set x axis tick font size, default 12.
        --ylfs int    Set y axis font size, default 12.
        --yr yrange   Set the yAxis plot range: float1,float2.
        --hl hline    Add horizontal lines: float1,float2.
        --ms msize    Set marker size: float, default 2.
        --bm bmargin  Bottom margin, default 40.
        --rm int      Right margin, default 20.
        --lm int      left margin, default 50.
        --over        Overlap dot with box.
        --nobox       Hidden box, only show dots.
        --nooutliers  Turn on the --over option, and hidden outliers, the Whiskers as the min/max.
        --ha hanno    Add horizontal line annotation with text.
                        format: x1_x2_y_text,x1_x2_y_text.
                        Example: 1_2_0.5_**
                        Each category for the box plot with x-coordinate as 0,1,2...n-1.
        --ady ady     Set the distance between horizontal annotation line and text (default 0.025).
        --haw float   Set the horizontal annotation line with, default 2.
        --hat int     Set the (horizontal or text) annotation font size, default 12.
        --atext txt   Add text annotations to the boxplot.
                        format: x1_y1_text,x2_y2_text.
                        Example: 1_0.5_**,
                        Each category for the box plot with x-coordinate as 0,1,2...n-1.
        --atr int     Set the annotation text rotation angle.
        --cl colors   Set the colors of the box plot, eg: '#1F77B4::#2B9D2B'.
        --ydt float   Set the tick distance on y axis.
        --c2          Set the input data format as 2 columns format.
        --yt txt      Tranform the scale of y, default no. Support: log.
        --ngy         No show grid line for Y axis. Default show Y grid background line.
        --sy          Show Y axis, default no show.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

        https://plot.ly/python/text-and-annotations/
        (API)https://plot.ly/python/reference/#layout-annotations
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
# input format 1
#------------------
c1  1   10  1
c2  2   -5  3
c3  5   3   2

# input format 2: --c2
#------------------
c1 1
c1 10
c1 3
c2 2
c2 5
c2 -1
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    print(args)
    errYCol = '' #value column for error bar for Y.
    xtitle = args['-x']
    ytitle = args['-y']
    outname = args['-o']
    mode = 'markers'
    hlines = [] #location for horizontal lines.
    vlines = []
    msize = 2
    overBoxDot = False #overlap box with dots.
    bmargin = 40 #  bottom margin.
    arowAnnotation = ''
    ady = 0.025
    haw = 2

    ydt = ''
    yrange = None
    if args['--yerr']:
        errYCol = int(args['--yerr']) -1
    if args['--yr']:
        yrange = list(map(float, args['--yr'].split(',')))
    if args['--hl']:
        hlines = list(map(float, args['--hl'].split(',')))
    if args['--ms']:
        msize = float(args['--ms'])
    if args['--over']:
        overBoxDot = True
        outliers_opacity = 1
    # only show dots, no show box.
    DOTS_ONLY = True if args['--nobox'] else False
    if DOTS_ONLY:
        overBoxDot = False
    # overlay box and dots, and hidden outliers.
    # This is just a workaround, may suffer change later on.
    # https://github.com/plotly/plotly.js/issues/1953
    if args['--nooutliers']:
        overBoxDot = True
        outliers_opacity = 0

    if args['--bm']:
        bmargin = int(args['--bm'])
    if args['--ha']:
        arowAnnotation = args['--ha']
    if args['--ady']:
        ady = float(args['--ady'])
    if args['--haw']:
        haw = float(args['--haw'])
    if args['--ydt']:
        ydt = float(args['--ydt'])
    hat = int(args['--hat']) if args['--hat'] else 12
    #angle for rotate x axis.
    rx = int(args['--rx']) if args['--rx'] else None
    ry = int(args['--ry']) if args['--ry'] else None
    xls = int(args['--xls']) if args['--xls'] else 12
    ylfs = int(args['--ylfs']) if args['--ylfs'] else 12
    rm = int(args['--rm']) if args['--rm'] else 20
    lm = int(args['--lm']) if args['--lm'] else 50
    transformY = args['--yt'] if args['--yt'] else 'linear' #tranform the scale of y.
    TextAnno = args['--atext'] if args['--atext'] else False
    TextAnnoRotation = int(args['--atr']) if args['--atr'] else 0

    format2 = True if args['--c2'] else False
    GRID_Y  = False if args['--ngy'] else True
    SHOWY = False
    YTICKLEN = 0
    if args['--sy']:
        SHOWY = True
        YTICKLEN = 5

    commands = {'vl'}
    data = [] #[[name, val1,val2 ..], [name, val1, val2...]]
    x_data = [] # [name1, name2]
    y_data = [] # [ [val1,val2 ..], [val1,val2 ..] ]
    from collections import OrderedDict
    data_map = OrderedDict() # categoryName -> [values]
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0]=='COMMAND' and ss[1] in commands:
                if ss[1] == 'vl':
                    vlines.append(float(ss[2]))
            else:
                if not format2:
                    x_data.append(ss[0])
                    y_data.append([float(x) for x in ss[1:]])
                else:
                    try:
                        y = float(ss[1])
                        if ss[0] not in data_map:
                            data_map[ss[0]] = []
                        data_map[ss[0]].append(y)
                    except ValueError:
                        sys.stderr.write('WARN: Parse ValueError, skipped: %s\n'%(line))

    if format2:
        # print(data_map)
        for k,v in data_map.items():
            x_data.append(k)
            y_data.append(v)

    #colors = ['rgba(93, 164, 214, 1)', 'rgba(255, 65, 54, 1)', 'rgba(44, 160, 101, 1)','rgba(255, 144, 14, 1)', 'rgba(207, 114, 255, 1)', 'rgba(127, 96, 0, 1)', 'rgba(255, 140, 184, 1)', 'rgba(79, 90, 117, 1)', 'rgba(222, 223, 0, 1)']
    colors = ['rgba(93, 164, 214,1)', 'rgba(255, 65, 54,1)', 'rgba(44, 160, 101,1)','rgba(255, 144, 14, 1)', 'rgba(207, 114, 255, 1)', 'rgba(127, 96, 0, 1)', 'rgba(255, 140, 184, 1)', 'rgba(79, 90, 117, 1)', 'rgba(222, 223, 0, 1)']
    #colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(44, 160, 101, 0.5)','rgba(255, 144, 14, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)', 'rgba(255, 140, 184, 0.5)', 'rgba(79, 90, 117, 0.5)', 'rgba(222, 223, 0, 0.5)']

    colors += colors
    colors += colors
    import plotly
    import plotly.plotly as py
    import plotly.graph_objs as go

    traces = []

    colors = colors[:len(x_data)]
    if args['--cl']:
        tcolors = args['--cl'].split('::')
        colors = []
        for i in range(len(x_data)):
            colors.append(tcolors[i%len(tcolors)])

    for xd, yd, cls in zip(x_data, y_data, colors):
            if overBoxDot:
                traces.append(go.Box(
                    y=yd,
                    name=xd,
                    # boxpoints=overBoxDot_points,
                    boxpoints='outliers',
                    whiskerwidth=0.2,
                    #fillcolor=cls,
                    marker=dict(
                        size=msize,
                        color = cls,
                        opacity = outliers_opacity
                    ),
                    line=dict(width=1),
                ))
            else:
                if DOTS_ONLY:
                    # https://codepen.io/etpinard/pen/NaVreM?editors=0010
                    traces.append(go.Box(
                        y=yd,
                        name=xd,
                        boxpoints='all',
                        whiskerwidth=0.2,
                        fillcolor='rgba(0,0,0,0)',
                        line= dict(color='rgba(0,0,0,0)'),
                        marker=dict(
                            size=msize,
                            color = cls
                        ),
                        # line=dict(width=1),
                    ))
                else:
                    traces.append(go.Box(
                        y=yd,
                        name=xd,
                        boxpoints='all',
                        jitter=0.5,
                        whiskerwidth=0.2,
                        #fillcolor=cls,
                        marker=dict(
                            size=msize,
                            color = cls
                        ),
                        line=dict(width=1),
                    ))

    ticktext=None
    tickvals=None
    if DOTS_ONLY:
        ticktext = x_data
        tickvals = [-0.3 + x for x in range(0,len(x_data))]
    # print(yrange)
    layout = go.Layout(
        #title='Points Scored by the Top 9 Scoring NBA Players in 2012',
        yaxis=dict(
            title=ytitle,
            type=transformY,
            # autorange=True,
            showgrid=GRID_Y,
            color   ='black',
            zeroline=False,
            # zeroline=True,
            tickangle=ry,
            dtick=ydt,
            showline=SHOWY,
            ticklen=YTICKLEN,
            # gridcolor='rgb(255, 255, 255)',
            #gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
            range=yrange,
            titlefont=dict(
                size = ylfs
            )
        ),
        xaxis=dict(
            ticks='outside',
            # zeroline=True,
            # tickvals=[-0.3,0.7],
            # ticktext=['c1','c2'],
            tickvals=tickvals,
            ticktext=ticktext,
            showline=True,
            tickangle=rx,
            color   ='black',
            tickfont=dict(
                size = xls
            )
        ),
        margin=dict(
            l=lm,
            r=rm,
            b=bmargin,
            t=10,
        ),
        # paper_bgcolor='rgb(243, 243, 243)',
        # plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )


    #https://plot.ly/python/text-and-annotations/
    #(API)https://plot.ly/python/reference/#layout-annotations
    # Each category for the box plot with x-coordinate as 0,1,2...n-1.
    annoArray = []
    # arowAnnotation="1_2_0.8_*"
    annoColor='black'
    # ady = 0.025
    if arowAnnotation:
        for x in arowAnnotation.split(','):
            ss = x.split('_')
            x1 = float(ss[0])
            x2 = float(ss[1])
            y  = float(ss[2])
            t  = ss[3]
            #draw a horizontal line
            annoArray.append(
                dict(
                    x=x1,
                    y=y,
                    xref='x',
                    yref='y',
                    #yref='paper',
                    text='',
                    showarrow=True,
                    arrowhead=0,
                    arrowwidth=haw,
                    arrowcolor=annoColor,
                    font=dict(
                        color=annoColor,
                        size = 12,
                    ),
                    # If `axref` is an axis, this is an absolute value on that axis, like `x`, NOT a relative value.
                    axref='x',
                    ax=x2,
                    ay=0
                ))
            #draw Font text.
            annoArray.append(dict(
                    x=(x1+x2)/2.0,
                    y=y + ady,
                    xref='x',
                    yref='y',
                    #yref='paper',
                    text=t,
                    showarrow=False,
                    arrowhead=0,
                    arrowcolor=annoColor,
                    font=dict(
                        color= annoColor,
                        size = hat,
                    ),
                    # # If `axref` is an axis, this is an absolute value on that axis, like `x`, NOT a relative value.
                    # axref='x',
                    # ax=float(ss[0])+1,
                    # ay=0
                ))

    # add text annotation
    if TextAnno:
        for x in TextAnno.split(','):
            ss = x.split('_')
            x1 = float(ss[0])
            y  = float(ss[1])
            t  = ss[2]

            # draw Font text.
            # https://plot.ly/python/reference/#layout-annotations
            annoArray.append(dict(
                    x=x1,
                    y=y,
                    xref='x',
                    yref='y',
                    #yref='paper',
                    text=t, textangle = TextAnnoRotation,valign='bottom',align='left',
                    xanchor='center',
                    showarrow=False,
                    arrowhead=0,
                    arrowcolor=annoColor,
                    font=dict(
                        color= annoColor,
                        size = hat,
                    ),
                ))

    annoLayout = go.Layout(
        annotations = annoArray
    )

    #fig['layout'].update(layout)accounts
    fig = go.Figure(data=traces, layout=layout)
    if annoArray:
        fig['layout'].update(annoLayout)

    #fig = go.Figure(data=traces, layout=layout)
    #py.iplot(fig)
    #output the last one
    # plotly.offline.plot({'data': traces,'layout': layout}
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
