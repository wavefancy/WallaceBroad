#!/usr/bin/env python3

"""

    Annotate bed file by gene's transcripts.

    @Author: wavefancy@gmail.com

    Usage:
        annotateBEDbyTranscripts.py [-l] -i file
        annotateBEDbyTranscripts.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Output results to stdout.
        2. *** Please make sure the chr coding matched between files, e.g. chr1 vs 1.
        3. The input bed file was designed as:
            cds1Start     -- cds1end,
            cds2start     -- cds2end,
            cds3start     -- cds2end,
            ...
            lastcdsstart  -- lastcdsend.

    Options:
        -i file       Input gtf db file.
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

    anno_map = {} # Annotation map: chr_cds1Start_cds1end -> [transcript_annotation, ...]
                  # transcript_annotation = (name ,n_cds, [cds1Start, cds1end, cds2start, cds2end ..., lastcdsstart, lastcdsend],genename)

    #load bed file and start compare.
    import numpy
    # bed = numpy.genfromtxt(sys.stdin,dtype='str')
    bed = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            bed.append(line.split())

    # The load inpu should be like the gencode gtf file.
    # The file should already have genes and transcripts on separate lines.
    # This means we can avoid the gene and transcript inference, which saves time.
    # merge_strategy='merge', use this to solve duplicate id issues.
    import gffutils
    # db = gffutils.create_db(args['-t'],
    # ":memory:",
    # keep_order=True,
    # merge_strategy="create_unique",
    # sort_attribute_values=True,
    # disable_infer_genes=True, disable_infer_transcripts=True)
    db = gffutils.FeatureDB(args['-i'], keep_order=True)

    #Iterate on genes
    for tt in db.features_of_type('transcript'):
        # print(tt['ID'])
        cds = list(db.children(tt, featuretype='CDS', order_by='start'))
        if cds:
            c = cds[0]
            # print(c)
            key='%s_%d_%s'%(c.seqid, int(c.start)-1, c.end)
            if key not in anno_map:
                anno_map[key] = []
            array = []
            for c in cds:
                array.append(int(c.start)-1)
                array.append(c.end)
            #add 3 bases for stop codon.
            array[-1] += 3
            array = '-'.join(map(str,array))
            anno_map[key].append((tt['transcript_id'][0],len(cds),array,tt['gene_name'][0]))
    # print(anno_map)
    # sys.exit(-1)

    i = 0
    while i < len(bed):
        # print('MYI:' + str(i))
        key = '_'.join(bed[i])
        found = False

        if key not in anno_map:
            sys.stderr.write('Failed: %s\n'%(key))
            i += 1
            # sys.exit(-1)
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
                array='-'.join(array)
                if args['-l']:
                    sys.stdout.write('bed: %s\n'%(array))
                    sys.stdout.write('gtf: %s\n'%(t[2]))
                if t[2] == array: #matched, output results.
                    for x in bed[i:j]:
                        sys.stdout.write('%s\t%s\t%s\n'%('\t'.join(x),t[-1],t[0]))

                    i = j
                    found = True
                    break
            #Iterate overall possible transcript, no candidate found.
            # print(i)
            if not found:
                sys.stderr.write('Failed: %s\n'%(key))
                i += 1
                # sys.stderr.write('ERROR: can not find any transcript start match this bed record, please check! >%s\n'%(key))
                # sys.exit(-1)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
