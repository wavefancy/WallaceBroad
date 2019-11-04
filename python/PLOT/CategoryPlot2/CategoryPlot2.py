#!/usr/bin/env python3

"""

    Plot category data using plotly library.
    @Author: wavefancy@gmail.com

    Usage:
        CategoryPlot2.py -x xtitle -y ytitle -o outname [--yerr ycol] [--yr yrange] [--vl vline] [--hl hline] [--ab abline] [--ms msize] [--mt mtype] [--lloc lloc] [--lfs lfs] [--lm lmargin] [--bm bmargin] [--tm topmargin] [--ydt float] [--xdt float] [--clr int] [--xta int] [--xr xrange] [--tfs int] [--ifs int] [--ctxt int] [--fl] [--flc color] [--op] [--cms int] [--font str] [--title txt]
        CategoryPlot2.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -x xtitle
        -y ytitle
        --title txt   Set the title for figure.
        -o outname    Output file name: output.html.
        --yerr yecol  Column index for y error bar. single valure or two values for lower and upper bound.
                        float | float1,float2 (lower,upper bound)
        --yr yrange   Set the yAxis plot range: float1,float2.
        --ydt float   Distance between y ticks.
        --xdt float   Distance between x ticks.
        --xr xrange   Set the xAxis plot range: float1,float2 | tight
                      tight: set the xrange as [xmin, xmax]
        --hl hline    Add horizontal lines: float1,float2.
        --vl vline    Add vertical lines: float1,float2...
        --ab abline   Add ablines: x1_y1_x2_y2_color;...
        --ms msize    Set marker size: float, default 5.
        --mt mtype    Set marker type: 1 dot(default), 2 line, 3 dot + line.
        --lloc lloc   Legend location:
                        1 left_top, 2 right_top, 3 left_bottom, 4 right_bottom, 0 no legend.
                        5 right_top out of box.
        --lfs lfs     Legend font size, default 10.
        --tfs int     X Y tick font size, default 12.
        --ifs int     X Y title font size, default 12.
        --lm lmargin  Left margin, default 50.
        --bm bmargin  Bottom margin, default 40.
        --tm topmargin Top margin, default 10.
        --clr int     Column index for color, 1 based.
        --ctxt int    Column index for text. This column can be empty for some group if it's the last column.
                      But all the points in non-empyt group should have text value, example: in.text.txt.
        --xta int     X ticks angle (rotate x ticks), eg 45.
        --cms int     Column index for marker symbol. Default: circle.
                          All of the supported symbols: https://plot.ly/python/reference/#scatter-marker-symbol
        --fl          Add a fitting line.
        --flc color   Fitting line color, default red.
        --op          Set open box, no right and top axis.
        --font str    Change the text font.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.
"""
# plotly api:
# chang xticks : https://plot.ly/python/axes/
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
# Output from: FamilyHitByGene.py
# groupAnnotation groupname annotationPair
# mt: marker symbol. https://plot.ly/python/reference/#scatter-marker-symbol
----------------------------
c1  1   10  1
c2  2   -5  3
c3  5   3   2
COMMAND vl  3
COMMAND vl  4
COMMAND xticktext       chr1    chr2
COMMAND xtickvals       150     550
COMMAND groupAnnotation C1 color:red ms:1 mt:'x'

    #output:
    ------------------------
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='3.8.1')
    # version 2.2: add the option for abline.
    print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    errYCol = '' #value column for error bar for Y.
    xtitle = args['-x']
    ytitle = args['-y']
    ftitle  = args['--title'] if args['--title'] else None  # Figure title.
    outname = args['-o']
    mode = 'markers' #markers or lines
    hlines = [] #location for horizontal lines.
    vlines = []
    msize = 5
    # lm = 50
    lm = None  #left margins
    bm = 40
    clrClm = ''  #value column for parse point color.
    xtickangle = None

    yrange = None
    ydt = '' # Distance between y ticks.
    xdt = '' # Distance between x ticks.
    Xrange = None
    groupAnnotation = {} # groupname -> {color:red, ms:2, ..}
    if args['--yerr']:
        errYCol = int(args['--yerr']) -1
    if args['--yr']:
        yrange = list(map(float, args['--yr'].split(',')))
    if args['--hl']:
        hlines = list(map(float, args['--hl'].split(',')))
    if args['--vl']:
        vlines = list(map(float, args['--vl'].split(',')))
    if args['--ms']:
        msize = float(args['--ms'])
    if args['--mt']:
        if args['--mt'] == '2':
            mode = 'lines'
        elif args['--mt'] == '3':
            mode = 'lines+markers'
    if args['--lm']:
        lm = float(args['--lm'])
    if args['--bm']:
        bm = float(args['--bm'])
    tm = float(args['--tm']) if args['--tm'] else 10   # topmargin.
    if args['--ydt']:
        ydt = float(args['--ydt'])
    if args['--xdt']:
        xdt = float(args['--xdt'])
    if args['--clr']:
        clrClm = int(args['--clr']) -1
    if args['--xta']:
        xtickangle = int(args['--xta'])
    if args['--xr']:
        if args['--xr'] == 'tight':
            Xrange = 'tight'
        else:
            Xrange = list(map(float, args['--xr'].split(',')))

    xanchor = 'right'
    yanchor = 'bottom'
    xlloc = 0.99
    ylloc = 0
    if args['--lloc']:
        if args['--lloc'] == '1':
            yanchor = 'top'
            xanchor = 'left'
            xlloc = 0.01
            ylloc = 0.99
        elif args['--lloc'] == '2':
            yanchor = 'top'
            xlloc = 0.99
            ylloc = 0.99
        elif args['--lloc'] == '3':
            yanchor = 'bottom'
            xanchor = 'left'
            xlloc = 0.01
            ylloc = 0.01
        elif args['--lloc'] == '4':
            yanchor = 'bottom'
            xanchor = 'right'
            xlloc = 0.99
            ylloc = 0.01

    ablines = []
    abcolor = '#EA3232' #line color for ablines, if not set from command line.
    if args['--ab']:
        for x in args['--ab'].split(';'):
            ablines.append(x.split('_'))

    lfontSize = 10
    if args['--lfs']:
        lfontSize = int(args['--lfs'])
    tickfontsize = 11
    if args['--tfs']:
        tickfontsize = int(args['--tfs'])
    titlefontsize = 12
    if args['--ifs']:
        titlefontsize = int(args['--ifs'])

    ctxt = '' #column index for display text.
    if args['--ctxt']:
        ctxt = int(args['--ctxt']) -1

    flcolor = 'red'
    if args['--flc']:
        flcolor = args['--flc']

    myMirror = True
    if args['--op']:
        myMirror = False

    cms = ''
    if args['--cms']:
        cms = int(args['--cms']) -1

    font = args['--font'] if args['--font'] else None

    # https://plot.ly/python/axes/
    # change x ticks
    #ticktext=labels,
    #tickvals=[i * step for i in range(len(labels))]
    xticktext = None
    xtickvals = None

    from collections import OrderedDict
    xdata = OrderedDict() #{categoryName -> []}
    ydata = OrderedDict() #{categoryName -> []}
    errY  = {} #{categoryName -> []} error bar for Y.ss
    pcolors = {} # {categoryName -> []} error bar for point colors.
    symbols = {} # for point symbol.
    ptxt = {} #for display text.
    commands = {'vl','xticktext','xtickvals','groupAnnotation'}

    def addData(dictName,keyName,val):
        '''add data to a dict'''
        if keyName not in dictName:
            dictName[keyName] = []
        dictName[keyName].append(val)

    xmin = 1000000000
    xmax = -100000000
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0]=='COMMAND' and ss[1] in commands:
                if ss[1] == 'vl':
                    vlines.append(float(ss[2]))
                if ss[1] == 'xticktext':
                    xticktext =[x if x != 'NA' else '' for x in ss[2:]]

                if ss[1] == 'xtickvals':
                    xtickvals = [float(x) for x in ss[2:]]
                if ss[1] == 'groupAnnotation':
                    g = ss[2]
                    groupAnnotation[g] = {}
                    for x in ss[3:]:
                        s = x.split(':')
                        groupAnnotation[g][s[0]] = s[1]

            else:
                try:
                    x = float(ss[1])
                    y = float(ss[2])
                    if errYCol and len(ss) >= errYCol +1:
                        #z = float(ss[errYCol])
                        z = ss[errYCol]
                        addData(errY,ss[0],z)

                    if clrClm:
                        addData(pcolors,ss[0], ss[clrClm])

                    if ctxt and len(ss) > ctxt:
                        addData(ptxt, ss[0], ss[ctxt])

                    if cms:
                        addData(symbols,ss[0], ss[cms])

                    addData(xdata, ss[0], x)
                    addData(ydata, ss[0] ,y)
                    if Xrange == 'tight':
                        if x < xmin:
                            xmin = x
                        if x > xmax:
                            xmax = x
                except ValueError:
                    sys.stderr.write('Warning: parse value error: %s\n'%(line))

    if Xrange == 'tight':
        Xrange = [xmin,xmax]

    plotData = []
    import plotly
    import plotly.plotly as py
    import plotly.graph_objs as go

    # print(msize)
    line = dict()
    if args['--mt'] == '2':
        marker = dict(
            # size = msize,
            line = dict(
                width = msize
                # color = 'white'
            )
         )
        line = dict(width = msize)
    else:
        marker = dict(
            size = msize
         )

    #print(pcolors)
    #print(xdata)
    for k in xdata.keys(): #data category.
        if cms: #set point markers.
            marker['symbol'] = symbols[k]
            # print(marker['symbol'])

        if k in errY:
            color = '#000000'
            size = 1
            if k in pcolors:
                marker['color'] = pcolors[k] #color, same length as the data set.
                line['color'] = pcolors[k][0]
                color = pcolors[k][0]
                #print(pcolors[k])

            #check and set commands
            if k in groupAnnotation:
                if 'color' in groupAnnotation[k]:
                    marker['color'] = groupAnnotation[k]['color']
                    line['color'] = groupAnnotation[k]['color']
                    color = groupAnnotation[k]['color']
                if 'ms' in groupAnnotation[k]:
                    marker['size'] = groupAnnotation[k]['ms']
                    line['width'] = groupAnnotation[k]['ms']
                    size = groupAnnotation[k]['ms']
                if 'mt' in groupAnnotation[k]:
                    marker['symbol'] = groupAnnotation[k]['mt']

            if len(errY[k][0].split(',')) == 2: # two values for error y.
                TY  = [x.split(',') for x in errY[k]]
                EY1 = [float(x[0]) for x in TY]
                EY2 = [float(x[1]) for x in TY]
                plotData.append(
                    go.Scatter(
                    x=xdata[k],
                    y=ydata[k],
                    name = k,
                    mode = mode,
                    marker = marker,
                    line = line,
                    error_y=dict(
                        type='data',
                        array = EY2,
                        arrayminus = EY1,
                        visible=True,
                        color=color,
                        thickness=size,
                        )
                ))

            else: #one value for error y.
                EY = [float(x) for x in errY[k]]
                plotData.append(
                    go.Scatter(
                    x=xdata[k],
                    y=ydata[k],
                    name = k,
                    mode = mode,
                    marker = marker,
                    line = line,
                    error_y=dict(
                        type='data',
                        array=errY[k],
                        visible=True,
                        color=color,
                        thickness=size,
                        )
                ))
        else:
            if k in pcolors:
                marker['color'] = pcolors[k] #color, same length as the data set.
                line['color'] = pcolors[k][0]
                #print(pcolors[k])

            #check and set commands
            if k in groupAnnotation:
                if 'color' in groupAnnotation[k]:
                    marker['color'] = groupAnnotation[k]['color']
                    line['color'] = groupAnnotation[k]['color']
                if 'ms' in groupAnnotation[k]:
                    marker['size'] = groupAnnotation[k]['ms']
                    line['width'] = groupAnnotation[k]['ms']
                if 'mt' in groupAnnotation[k]:
                    marker['symbol'] = groupAnnotation[k]['mt']
            #print(marker)
            #print(line)
            if k in ptxt:
                plotData.append(
                    go.Scatter(
                    x=xdata[k],
                    y=ydata[k],
                    marker = marker,
                    text = ptxt[k],
                    line = line,
                    name=k,
                    mode = mode + '+text',
                    textfont=dict(size=10),
                    textposition='top',
                ))

            else:
                plotData.append(
                    go.Scatter(
                    x=xdata[k],
                    y=ydata[k],
                    marker = marker,
                    line = line,
                    name=k,
                    mode = mode,
                ))

    # print(plotData)
    #add a fit line
    if args['--fl']:
        #ref: https://plot.ly/python/linear-fits/
        #ref: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html
        from numpy import arange,array
        from scipy import stats
        allData = []
        for k in xdata.keys():
            for x,y in zip(xdata[k],ydata[k]):
                allData.append((x,y))

        #sort data by x
        allData = sorted(allData,key=lambda x:x[0])
        x = array([x[0] for x in allData])
        y = array([x[1] for x in allData])
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        line = slope*x+intercept

        plotData.append(go.Scatter(
                  x=x,
                  y=line,
                  mode='lines',
                  marker=go.Marker(color=flcolor),
                  name='Fit Line'
                  )
            )
    #print(xticktext)
    #print(xtickvals)
    layout = {
        'title': ftitle,
        'font': {'family':font},
        'margin': {
            'l' : lm,
            'b' : bm,
            'r' : 10,
            't' : tm
        },
        'xaxis':{
            'dtick'   : xdt,
            'mirror'  : myMirror,
            'range'   : Xrange,
            'color'   :'black',
            #       range=[0, 500],
            'showgrid':True,
            'showline':True,
            'ticks'   : 'outside',
            'showticklabels' : True,
            'title'   : xtitle,
            'zeroline':False,
            'ticktext':xticktext,
            'tickvals':xtickvals,
            'tickangle': xtickangle,
            'tickfont': {
                #family: 'Courier New, monospace',
                'size': tickfontsize,
                #color: '#7f7f7f'
            },
            'titlefont': {
                #family: 'Courier New, monospace',
                'size': titlefontsize,
                #color: '#7f7f7f'
            },
        },
    }
    # update legend info.
    legend={
        'showlegend': False
    }
    # api: https://plot.ly/python/legend/
    if args['--lloc'] != '0':
        if args['--lloc'] == '5':
            # legend = go.Layout(
            #     showlegend=True
            # )
            legend={
                'legend':{
                    'font': {
                        'size' : lfontSize
                    },
                }
            }
        else:
            legend={
                'legend':{
                    'xanchor': xanchor,
                    'x': xlloc,
                    'y': ylloc,
                    'yanchor': yanchor,
                    'font': {
                        'size' : lfontSize
                    },
                }
            }

    #print(legend)
    layout.update(legend)

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
                        'dash': 'dashdot',
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

    vl_data = []
    if vlines:
        for y in vlines:
            vl_data.append(
                {
                    'type': 'line',
                    'yref': 'paper',
                    'x0': y,
                    'y0': 0,
                    'x1': y,
                    'y1': 1,
                    'line': {
                        'color': '#FFD979',
                        'width': 2,
                        'dash': 'dashdot',
                }}
            )
        #h = {'shapes':vl_data}
        #layout.update(h)
    alllines = hl_data + vl_data + ab_data
    if alllines:
        h = {'shapes':alllines}
        layout.update(h)

    yudict = dict(
        dtick = ydt, # '' empty string means auto ticks
        # autotick = True,
        mirror  = myMirror,
        range   =yrange,
        color   ='black',
        # showgrid = True,
        showline = True,
        ticks =  'outside',
        showticklabels = True,
        title = ytitle,
        zeroline = False,
        titlefont=dict(size=titlefontsize),
        tickfont = {
            #family: 'Courier New, monospace',
            'size': tickfontsize,
            #color: '#7f7f7f'
        }
    )
    # layout.update(yupdate)
    layout['yaxis'] = yudict
    #output the last one
    plotly.offline.plot({'data': plotData,'layout': layout}
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
