#!/usr/bin/env python3

"""

    Map color based on input value.
    @Author: wavefancy@gmail.com

    Usage:
        Value2ColorV2.py -k int [-r] [-n cname] [-g cgroup] [--rl float] [--rr float] [-s txt]
        Value2ColorV2.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -k int        Color index for input value.
        --rl float    Set color range left end, default min(inputValues).
        --rr float    Set color range right end, default max(inputValues).
        -r            Reverse color map.
        -n cname      Color scale name, default YlGnBu_4, full list:
                      https://jiffyclub.github.io/palettable/colorbrewer/
        -g cgroup     Set color group, default sequential. [sequential|diverging|qualitative]
        -s txt        Output color as a single line array, array elements separated by 'txt'.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

    API:
        Palette names please ref. https://jiffyclub.github.io/palettable/#matplotlib-colormap
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
c1  1   10  1
c2  2   -5  3
c3  5   3   2
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    # add regression line to scatter plot
    # https://plot.ly/python/linear-fits/

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    singeLine=  ''
    if args['-s']:
        singeLine = args['-s']
    col = int(args['-k']) -1
    indata = []
    zcolor = []
    opacity = 1
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                x = float(ss[col])

                indata.append(ss)
                zcolor.append(x)

            except ValueError:
                sys.stdout.write('Warning: Parse Value Error (Skipped): %s\n'%(line))

    # https://stackoverflow.com/questions/3279560/invert-colormap-in-matplotlib
    import matplotlib as mpl
    def reverse_colourmap(cmap, name = 'my_cmap_r'):
        """
        In:
        cmap, name
        Out:
        my_cmap_r

        Explanation:
        t[0] goes from 0 to 1
        row i:   x  y0  y1 -> t[0] t[1] t[2]
                       /
                      /
        row i+1: x  y0  y1 -> t[n] t[1] t[2]

        so the inverse should do the same:
        row i+1: x  y1  y0 -> 1-t[0] t[2] t[1]
                       /
                      /
        row i:   x  y1  y0 -> 1-t[n] t[2] t[1]
        """
        reverse = []
        k = []

        for key in cmap._segmentdata:
            k.append(key)
            channel = cmap._segmentdata[key]
            data = []

            for t in channel:
                data.append((1-t[0],t[2],t[1]))
            reverse.append(sorted(data))

        LinearL = dict(zip(k,reverse))
        my_cmap_r = mpl.colors.LinearSegmentedColormap(name, LinearL)
        return my_cmap_r

    #API ref: https://stackoverflow.com/questions/28752727/map-values-to-colors-in-matplotlib
    #API ref: https://jiffyclub.github.io/palettable/colorbrewer/sequential/#previews
    #API ref: https://matplotlib.org/api/cm_api.html
    cname = 'YlGnBu_4'
    cgroup = 'sequential'
    if args['-n']:
        cname = args['-n']
    if args['-g']:
        cgroup = args['-g']
    #from palettable.colorbrewer.sequential import YlGnBu_4 as mycl
    exec('from palettable.colorbrewer.%s import %s as mycl'%(cgroup,cname))
    #import palettable.colorbrewer.sequential.YlGnBu_4 as mycl
    #import matplotlib
    import matplotlib.cm as cm
    #ax.imshow(data, cmap=Blues_8.mpl_colormap)

    vrange=[min(zcolor), max(zcolor)]
    if args['--rl']:
        vrange[0] = float(args['--rl'])
    if args['--rr']:
        vrange[1] = float(args['--rr'])

    norm = mpl.colors.Normalize(vmin=vrange[0], vmax=vrange[1], clip=True)
    mycolormap = mycl.mpl_colormap
    if args['-r']:
        mycolormap = reverse_colourmap(mycolormap)
    mapper = cm.ScalarMappable(norm=norm, cmap=mycolormap)
    #print(mycl.mpl_colormap._segmentdata)

    # if args['-r']:
    #     for x, y in zip(indata, oColor):
    #         x[col] = y
    #         sys.stdout.write('%s\n'%('\t'.join(x)))
    # else:
    out = []
    for x,y in zip(indata, zcolor):
        if singeLine:
            out.append('rgba'+str(mapper.to_rgba(y,alpha=opacity,bytes=True,norm=True)).replace(' ',''))
        else:
            x.append('rgba'+str(mapper.to_rgba(y,alpha=opacity,bytes=True,norm=True)).replace(' ',''))
            sys.stdout.write('%s\n'%('\t'.join(x)))

    if out:
        sys.stdout.write('%s\n'%(singeLine.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
