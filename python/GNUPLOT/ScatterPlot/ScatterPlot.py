#!/usr/bin/env python3

"""

    Generate scatter plot

    @Author: wavefancy@gmail.com

    Usage:
        ScatterPlot.py -o out -s size [-c code] [-x xlabel] [-y ylabel] [-t int] [--vl txt] [--code] [--debug] [--ps float] [--lw float] [--lt int] [--pt int] [--sb]
        ScatterPlot.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output pdf file.
        2. Shape type code refer: https://stackoverflow.com/questions/19412382/gnuplot-line-types

    Options:
        -o out        Output file name.
        -s size       Output figure size in inch, width-height.
        -x xlabel     Set the x-label
        -y ylabel     Set the y-label
        -c code       Add gnuplot code, inserting position just before the plot function call.
                        eg. 'line1::line2'
        --ps float    Point size, default 1.
        --lw float    Line width, default 1.
        --lt int      Line type, default 1.
        --pt int      Point type, default 7.
        -t int        Plot type, 1:lines+points, 2:points, 3:lines. eg. 1(default)|2|3.
        --sb          Add a smooth line by gnuplot bezier function.
        --vl txt      Add vertical line(s), loc-attribute. 'loc-lt 1 lw 2 lc "red",loc-lt 1 lw 2 lc "blue"'
        --code        Output code to stderr.
        --debug       In debug model, keep temp files and output code to stderr.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
import tempfile
import numpy as np
import subprocess
# from subprocess import PIPE, CalledProcessError, check_output, Popen
import os
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    #input:
    ------------------------
    ''');

CODE_FILE = None
OUT_CODE = False
def w(code, Newline=True):
    '''write gnuplot code to tempfile'''
    c = code + '\n' if Newline else code
    CODE_FILE.write(c)
    if OUT_CODE:
        sys.stderr.write(c)

def runGNUPLOT(code_file):
    '''run generated code by gnuplot'''
    # sub = subprocess.check_output("gnuplot "+ code_file,shell=True)
    try:
        sub = subprocess.check_output("gnuplot "+ code_file,shell=True)
    except CalledProcessError as e:
        print(e.message)

#overlap the one from gnuplot, which is not compatible with gnuplot 5.0
def pdf(filename='tmp.pdf', width=14, height=9, fontsize=12, term='wxt'):
    '''Script to make gnuplot print into a pdf file, figure size in inch.
    Call this function at the begin of the plot.
    >>> pdf(filename='myfigure.pdf')  # overwrites/creates myfigure.pdf
    '''
    w('#!/usr/bin/gnuplot')
    w('reset')
    # w('set term pdf enhanced size ' + str(width) + 'in, ' + str(height) + 'in lw 2 font ' + " 'Sans-serif,"+str(fontsize)+"';")
    w('set term pdf enhanced size ' + str(width) + 'in, ' + str(height) + 'in lw 2 font ' + " 'Aril,"+str(fontsize)+"';")
    w('set out "' + filename + '";')
    # gp.c('replot;')
    # gp.c('set term ' + str(term) + '; replot')

    # grid
    # http://www.gnuplotting.org/calculating-histograms/
    # http://gnuplot.sourceforge.net/demo/dashtypes.html
    w("set style line 12 lc rgb'#d9d9d9' lw 1 dt '-'")
    w("set grid back ls 12")
    w("set grid xtics ytics mxtics")
    w("set tics nomirror out scale 1")

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    OUTNAME = args['-o']
    OUT_CODE = True if args['--code'] else False
    DEL_TEMP = True
    if args['--debug']:
        DEL_TEMP = False
        OUT_CODE = True

    VLINES = []
    if args['--vl']:
        for x in args['--vl'].split(','):
            VLINES.append(x.split('-'))
    fsize = args['-s'].split('-')
    XLABEL = args['-x'] if args['-x'] else None
    YLABEL = args['-y'] if args['-y'] else None
    CODE   = args['-c'].split('::') if args['-c'] else None
    ptypes =  ['linespoints', 'points','lines']
    plott = int(args['-t']) if args['-t'] else 1
    plott = ptypes[plott-1] #shift to 0 based.
    ps = args['--ps'] if args['--ps'] else '1.0'
    lw = args['--lw'] if args['--lw'] else '1.0'
    pt = args['--pt'] if args['--pt'] else '7'
    lt = args['--lt'] if args['--lt'] else '1'
    SMOOTH = True if args['--sb'] else None

    CODE_FILE = tempfile.NamedTemporaryFile(mode='w',dir="./",delete=DEL_TEMP)
    DATA_FILE = tempfile.NamedTemporaryFile(mode='w',dir="./",delete=DEL_TEMP)
    # fit a density use gnuplot Gaussian kernels. 'kdensity'
    # convert input array as histogram
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html
    # a = 50*np.random.rand() * np.random.normal(10, 10, 100) + 20
    # hist,bins = np.histogram(a,bins = 'auto', density=True)
    # len(bins) = len(hist) +1, as bins is the bundary.
    # n_bins = [(bins[i]+bins[i+1])/2.0 for i in range(len(bins)-1)]
    # gp.s([n_bins, hist])

    # INPUT data should be sorted by category.
    CATE_NAME = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if not CATE_NAME:
                CATE_NAME.append(ss[0])
            if ss[0] != CATE_NAME[-1]:
                CATE_NAME.append(ss[0])
                DATA_FILE.write('\n\n') # start a new data section.

            DATA_FILE.write('%s\n'%('\t'.join(ss[1:])))

    DATA_FILE.flush()

    # kernal density by gnuplot
    # gp.s([a])
    pdf(filename=OUTNAME, width=fsize[0], height=fsize[1], fontsize=23, term='pngcairo')
    #gp.c('plot "tmp.dat" u 1:2 w lp')
    # plot curve shape.

    # add vertical line
    for x in VLINES:
        # w('set arrow from 100,graph 0 to 100,graph 1 nohead lt 1 lw 2 lc "red"')
        w('set arrow from %s,graph 0 to %s,graph 1 nohead %s'%(x[0],x[0],x[1]))

    #samplen set the length of the legend, default 4
    w('set key left')
    if YLABEL:
        w('set ylabel "%s" offset 1,0,0'%(YLABEL)) #offset 1 move right
    if XLABEL:
        w('set xlabel "%s" offset 0,0.5,0'%(XLABEL))
    # only use left and bottom border
    w('set border 3 lw 1.5')

    COLORS = ['#0060ad','#dd181f']
    #COLORS = ['#5da4d6', '#ff900e','#272ca0']
    # line style index starts from 90
    for i in range(len(CATE_NAME)):
        w('set style line 9%d lc "%s" lt %s lw %s pt %s ps %s'%(i, COLORS[i%len(COLORS)], lt ,lw, pt, ps))

    # addittion code to insert.
    if CODE:
        [w(x) for x in CODE]

    # plot the figure.
    # w('plot "%s" index 0 with %s ls 90 title "%s"'%(DATA_FILE.name, plott, CATE_NAME[0]), Newline=False)
    w('plot "%s" index 0 with %s ls 90 title "%s"'%(DATA_FILE.name, plott, CATE_NAME[0]), Newline=False)
    if SMOOTH:
        w(', \\')
        w('"%s" index 0 with %s ls 90 notitle smooth bezier'%(DATA_FILE.name, plott), Newline=False)

    CATE_NAME = CATE_NAME[1:]
    for i,v in zip(range(len(CATE_NAME)), CATE_NAME):
        w(', \\')
        w("'' index %d with %s ls 9%d title '%s' "%(i+1, plott, i+1, v), Newline=False)
        if SMOOTH:
            w(', \\')
            w("'' index %d with %s ls 9%d notitle smooth bezier "%(i+1, plott, i+1), Newline=False)

    CODE_FILE.flush()
    runGNUPLOT(CODE_FILE.name)

CODE_FILE.close()
DATA_FILE.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
