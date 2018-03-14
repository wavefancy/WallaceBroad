#!/usr/bin/env python3

"""

    Annotate bed file by gene's transcripts.

    @Author: wavefancy@gmail.com

    Usage:
        annotateBEDbyTranscripts.py -t file [-l]
        annotateBEDbyTranscripts.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read input bed from stdin, and output results to stdout.
        2. *** Please make sure the chr coding matched between files, e.g. chr1 vs 1.
        3. The input bed file was designed as:
            cdsStart         -- 1 exon end,
            2 exon start     -- 2 exon end,
            3 exon start     -- 3 exon end,
            ...
            last exon start --- cds End.

    Options:
        -t file       Transcripts annotation file.
        -l            Output matching log to stderr.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

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
    # print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    anno_map = {} # Annotation map: chr_cdsStart_exon_1_end -> [transcript_annotation, ...]
                  # transcript_annotation = (name ,n_exons, [cdsStart, exon_1_start, exon_2_stat, exon_2_end ..., last_exon_start, cds_end],genename)
    with open(args['-t'],'r') as infile:
        for line in infile:
            line = line.strip()
            # print(line)
            if line:
                ss = line.split()
                exonstarts=ss[9][:-1].split(',')[1:] #skip the first exon_1_start
                exonends = ss[10][:-1].split(',')[:-1] #skip the last_exon_end.

                exonstarts = [ss[6]] + exonstarts #cdsStart
                exonends = exonends + [ss[7]]     #cds_end

                # ss[2] = ss[2][3:] if ss[2].lower().startswith('chr') else ss[2]
                key = '%s_%s_%s'%(ss[2],exonstarts[0],exonends[0])
                if key not in anno_map:
                    anno_map[key] = []

                array = []
                for x,y in zip(exonstarts, exonends):
                    array.append(x)
                    array.append(y)
                anno_map[key].append((ss[1], len(exonstarts),array,ss[12]))

    # print(anno_map)
    #load bed file and start compare.
    import numpy
    bed = numpy.genfromtxt(sys.stdin,dtype='str')
    i = 0
    while i < len(bed):
        # print('MYI:' + str(i))
        key = '_'.join(bed[i])
        found = False

        if key not in anno_map:
            sys.stderr.write('ERROR: can not find any transcript start match this bed record, please check! >%s\n'%(key))
            sys.exit(-1)
        else:
            transcripts = anno_map[key]
            for t in transcripts:
                n_exons = t[1]
                j = i + n_exons
                array = []
                for x in bed[i:j]:
                    array.append(x[1])
                    array.append(x[2])
                #output
                if args['-l']:
                    sys.stdout.write('bed\t%s\n'%('\t'.join(array)))
                    sys.stdout.write('tpt\t%s\n'%('\t'.join(t[2])))
                if t[2] == array: #matched, output results.
                    for x in bed[i:j]:
                        sys.stdout.write('%s\t%s\t%s\n'%('\t'.join(x),t[0],t[-1]))

                    i = j
                    found = True
                    break
            #Iterate overall possible transcript, no candidate found.
            # print(i)
            if not found:
                sys.stderr.write('ERROR: can not find any transcript start match this bed record, please check! >%s\n'%(key))
                sys.exit(-1)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
