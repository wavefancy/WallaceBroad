#!/usr/bin/env python

"""

    Fit the function a * exp(-x/b) + c

    @Author: wavefancy@gmail.com

    Usage:
        FitFunc.py [-p]
        FitFunc.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout.
            The fitted coefficient, a, b, c and the intercept of x of
            the tangent line at the point of (y=0) for the fitted curve.
        2. Output results from stdout.

    Options:
        -p            Generate predicted values based on the fitting function to stderr.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
#   Ref:
#        1. https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
#
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''Input File format example:'''
    print('''
#input example
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    import numpy as np
    from scipy.optimize import curve_fit

    def func(x, a, b, c):
        return a * np.exp(-x / b) + c

    def deriv(x, a, b, c):
        '''Compute the derivative of f at the point of x'''
        # http://math-physics-problems.wikia.com/wiki/Graphing_Tangent_Lines_with_Python
        h = 0.000000001                 #step-size
        y1 = func(x, a, b, c)
        y2 = func(x+h, a, b, c)
        # return (f(x+h) - f(x))/h        #definition of derivative
        return (y2-y1)/h        #definition of derivative

    data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                d = [float(x) for x in ss]
                data.append(d)
            except Exception as e:
                pass

    sys.stdout.write('a\tb\tc\tInterceptX_Y=0\n')
    data = np.array(data)
    f_vals = [] # [] fitted values of each fitted func.
    f_vals.append(data[:,0])
    # print(data)
    for i in range(1,len(data[0,:])):
        popt, pcov = curve_fit(func, data[:,0], data[:,i])
        out = [x for x in popt]

        #compute the intercept point of x when Y = 0
        #(y-y1)/(x-x1) = slop
        x = (0 - func(0,popt[0],popt[1],popt[2]))/deriv(0, popt[0],popt[1],popt[2]) + 0
        out.append(x)

        sys.stdout.write('%s\n'%('\t'.join(['%.4e'%(x) for x in out])))

        if args['-p']:
            fv = [func(x,popt[0],popt[1],popt[2]) for x in data[:,0]]
            f_vals.append(fv)

    if args['-p']:
        f_vals = np.array(f_vals).T
        for y in f_vals:
            sys.stderr.write('%s\n'%('\t'.join(['%.4e'%(x) for x in y])))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
