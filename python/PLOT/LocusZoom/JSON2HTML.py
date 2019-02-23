#!/usr/bin/env python3

"""

    Generate HTML page for LocusZoom plot.

    @Author: wavefancy@gmail.com

    Usage:
        JSON2HTML.py -r txt -j files
        JSON2HTML.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read sigle family ped file from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -r txt        Specify the region to plot.
        -j files      Jsons files to show in the plot.

        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
import json
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
#input example
------------------------
c1  1
c2  2
c3  5
    ''');


if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    basehtml = 'core_template.html'

    region = args['-r']
    jsons = args['-j'].split(',')


    # <div id="lz-plot-0" data-region="1:150010660-151010660"></div>
    # <div id="lz-plot-1" data-region="1:150010660-151010660"></div>
    # <div id="lz-plot-2" data-region="1:150010660-151010660"></div>
    out_region = []
    for i in range(len(jsons)+1):
        out_region.append('<div id="lz-plot-%d" data-region="%s"></div>'%(i, region))

    # var data_sources_2 = new LocusZoom.DataSources()
    #     .add("assoc", ["AssociationLZ", {url: "./json.MIG-1-150510660.json?", params: {analysis: 3, id_field: "variant"}}])
    #     .add("ld", ["LDLZ2", { url: "https://portaldev.sph.umich.edu/ld/" }])
    #     .add("gene", ["GeneLZ", { url: apiBase + "annotation/genes/" }])
    #     .add("recomb", ["RecombLZ", { url: apiBase + "annotation/recomb/results/" }])
    #     .add("constraint", ["GeneConstraintLZ", { url: "http://exac.broadinstitute.org/api/constraint" }]);
    out_resources = []
    for i,j in zip(range(len(jsons)),jsons):
        out_resources.append('''var data_sources_'''+str(i)+''' = new LocusZoom.DataSources()
    .add("assoc", ["AssociationLZ", {url: "'''+j+'''?", params: {analysis: 3, id_field: "variant"}}])
    .add("ld", ["LDLZ2", { url: "https://portaldev.sph.umich.edu/ld/" }])
    .add("gene", ["GeneLZ", { url: apiBase + "annotation/genes/" }])
    .add("recomb", ["RecombLZ", { url: apiBase + "annotation/recomb/results/" }])
    .add("constraint", ["GeneConstraintLZ", { url: "http://exac.broadinstitute.org/api/constraint" }]);''')

    # window.plot = LocusZoom.populate("#lz-plot", data_sources, layout_asso_only);
    # window.plot = LocusZoom.populate("#lz-plot-2", data_sources_2, layout_asso_only);
    # window.plot = LocusZoom.populate("#lz-plot-3", data_sources, layout_gene_only);
    out_plot=[]
    for i in range(len(jsons)):
        out_plot.append('window.plot = LocusZoom.populate("#lz-plot-%d", data_sources_%d, layout_asso_only);'%(i,i))
    i = len(jsons)
    out_plot.append('window.plot = LocusZoom.populate("#lz-plot-%d", data_sources_0, layout_gene_only);'%(i))

    with open(basehtml,'r') as bf:
        for line in bf:
            line = line.replace('__out_region__','\n'.join(out_region))
            line = line.replace('__out_resources__','\n'.join(out_resources))
            line = line.replace('__out_plot__','\n'.join(out_plot))
            sys.stdout.write('%s'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
