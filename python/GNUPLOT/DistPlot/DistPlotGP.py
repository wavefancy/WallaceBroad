#!/usr/bin/env python3

"""

    Generate distribution plot by pygnuplot

    @Author: wavefancy@gmail.com

    Usage:
        DistPlotGP.py -o out -s size [-c code] [-x xlabel] [--shade txt] [--vl txt] [--code] [--debug]
        DistPlotGP.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output pdf file.

    Options:
        -o out        Output file name.
        -s size       Output figure size in inch, width-height.
        -x xlabel     Set the x-label
        -c code       Add gnuplot code, inserting position just before the plot function call.
                        eg. 'line1::line2'
        --shade txt   Add shaing area annotation, 'left-right-color-title,left-right-color-title'.
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
def w(code):
    '''write gnuplot code to tempfile'''
    CODE_FILE.write(code+'\n')
    if OUT_CODE:
        sys.stderr.write(code+'\n')

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

    #shading area annotation.
    SHADE = []
    if args['--shade']:
        for x in args['--shade'].split(','):
            SHADE.append(x.split('-'))
    VLINES = []
    if args['--vl']:
        for x in args['--vl'].split(','):
            VLINES.append(x.split('-'))
    fsize = args['-s'].split('-')
    XLABEL = args['-x'] if args['-x'] else None
    CODE   = args['-c'].split('::') if args['-c'] else None

    CODE_FILE = tempfile.NamedTemporaryFile(mode='w',dir="./",delete=DEL_TEMP)
    DATA_FILE = tempfile.NamedTemporaryFile(mode='w',dir="./",delete=DEL_TEMP)
    SMOOTH_FILE = tempfile.NamedTemporaryFile(mode='w',dir="./",delete=DEL_TEMP)
    # fit a density use gnuplot Gaussian kernels. 'kdensity'
    # convert input array as histogram
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html
    # a = 50*np.random.rand() * np.random.normal(10, 10, 100) + 20
    # hist,bins = np.histogram(a,bins = 'auto', density=True)
    # len(bins) = len(hist) +1, as bins is the bundary.
    # n_bins = [(bins[i]+bins[i+1])/2.0 for i in range(len(bins)-1)]
    # gp.s([n_bins, hist])
    NUM_line = 0
    for line in sys.stdin:
        DATA_FILE.write(line)
        NUM_line += 1
    DATA_FILE.flush()

    # kernal density by gnuplot
    # gp.s([a])
    pdf(filename=OUTNAME, width=fsize[0], height=fsize[1], fontsize=23, term='pngcairo')
    #gp.c('plot "tmp.dat" u 1:2 w lp')
    # plot curve shape.
    w("set linetype 1 linecolor rgb '#0060ad' lw 2  # blue ")
    # set the transparent of filled area.
    w('set style fill transparent solid 0.8 noborder')
    if SHADE:
        for x,i in zip(SHADE,range(len(SHADE))):
            # w("set linetype 2%d linecolor rgb '%s' lw 2"%(i, x[2]))
            w("set linetype 2%d linecolor rgb '%s' "%(i, x[2]))

    w("set table '%s'"%(SMOOTH_FILE.name))
    # w('plot "tmp.dat" u 1:(1.0/%s) smooth kdensity'%(len(a)))
    w('plot "%s" u 1:(1.0/%d) smooth kdensity'%(DATA_FILE.name,NUM_line))
    w('unset table')
    w('filter(x,min,max) = (x > min && x < max) ? x : 1/0')
    # w('plot "data-smoothed" u 1:2 with lines lt 1 notitle')

    # add vertical line
    for x in VLINES:
        # w('set arrow from 100,graph 0 to 100,graph 1 nohead lt 1 lw 2 lc "red"')
        w('set arrow from %s,graph 0 to %s,graph 1 nohead %s'%(x[0],x[0],x[1]))

    #samplen set the length of the legend, default 4
    w('set key left samplen 1')
    w('set ylabel "Density" offset 1,0,0') #offset 1 move right
    if XLABEL:
        w('set xlabel "%s" offset 0,0.5,0'%(XLABEL))
    # only use left and bottom border
    w('set border 3 lw 1.5')

    # addittion code to insert.
    if CODE:
        [w(x) for x in CODE]

    if SHADE:
        # w("plot '%s' using (filter($1, 50, 100)):2 with filledcurves x1 lt 22 title 'T_1',\\"%(SMOOTH_FILE.name))
        x = SHADE[0];i=0
        w("plot '%s' using (filter($1, %s, %s)):2 with filledcurves x1 lt 2%d title '%s',\\"%(SMOOTH_FILE.name,x[0],x[1],i,x[3]))
        SHADE = SHADE[1:]
        for x,i in zip(SHADE,range(len(SHADE))):
            w(" '' using (filter($1, %s, %s)):2 with filledcurves x1 lt 2%d title '%s',\\"%(x[0],x[1],i+1,x[3]))
        w("'' using 1:2 with lines lw 3 lt 1 notitle")

    else:
        w("plot '%s' using 1:2 with lines lw 3 lt 1 notitle"%(SMOOTH_FILE.name))

    CODE_FILE.flush()
    runGNUPLOT(CODE_FILE.name)

CODE_FILE.close()
DATA_FILE.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
