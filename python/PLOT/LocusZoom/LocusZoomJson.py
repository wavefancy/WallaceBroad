#!/usr/bin/env python3

'''

    Generate JSON data for locus zoom.

    @Author: wavefancy@gmail.com, Wallace Wang.

    Usage:
        LocusZoomJson.py
        LocusZoomJson.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. Input as 5 colums: CHR POS REF ALT P_Value
        3. Set the minimal P values as 1e-80.

    Options:
        -h --help     Show this screen.
        --version     Show version.
        -f --format   Show input/output file format example.

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.
from docopt import docopt

def ShowFormat():
    '''File format example'''
    print('''
#Input as 5 colums: CHR POS REF ALT P_Value
------------------------
Sample  T1      T2      T3
ID1     1       2       3
ID2     4       5       1
ID3     7       3       1
ID4     2       1       4
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # sys.stdout.write(str(args)+'\n')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    import json
    import numpy
    data_map = {
        'analysis':[],
        'variant':[],
        'chr':[],
        'position':[],
        'refAlleleFreq':[],
        'ref_allele':[],
        'pvalue':[],
        'log_pvalue':[],
        'scoreTestStat':[]
                }

    def addValue(chr, pos, ref, alt, p):
        'add a single value to data_map'
        data_map['analysis'].append(3)
        data_map['variant'].append(chr+':'+pos+'_'+ref+'/'+alt)
        data_map['chr'].append(chr)
        # it's very import to make the pos as int, otherwise the linkage with not work.
        data_map['position'].append(int(pos))
        data_map['refAlleleFreq'].append('null')
        data_map['ref_allele'].append(ref)
        data_map['pvalue'].append(p)
        pp = float(p)
        pp = pp if pp > 1e-80 else 1e-80
        data_map['log_pvalue'].append(-1.0*numpy.log10(pp))
        data_map['scoreTestStat'].append('null')

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            addValue(ss[0],ss[1],ss[2],ss[3],ss[4])

    sys.stdout.write('%s\n'%(json.dumps({'data':data_map, 'lastPage':'null'})))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
