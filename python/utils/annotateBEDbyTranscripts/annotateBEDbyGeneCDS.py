#!/usr/bin/env python3

"""

    Annotate bed file according to gene's cds region,increase mapptability check both ends separatedly.

    @Author: wavefancy@gmail.com

    Usage:
        annotateBEDbyGeneCDS.py -i file
        annotateBEDbyGeneCDS.py -h | --help | -v | --version | -f | --format

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

    anno_map = {} # Annotation map: chr_cdsStart_cdsend -> set(gene_name)

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
        stop_codons = list(db.children(tt, featuretype='stop_codon', order_by='start'))
        # print(stop_codons)
        all = cds + stop_codons
        if all:
            # c = cds[0]
            # print(c)
            for c in all:
                # print(c)
                keys = ['%s_%d'%(c.seqid, int(c.start)-1),'%s_%s'%(c.seqid, c.end)]
                for key in keys:
                    if key not in anno_map:
                        anno_map[key] = set()

                    anno_map[key].add(tt['gene_name'][0])

    # print(anno_map)
    # sys.exit(-1)

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()

            key1 = '_'.join(ss[:2])
            key2 = '_'.join([ss[0],ss[2]])

            out = []
            for key in (key1, key2):
                if key in anno_map:
                    out.append(anno_map[key])
                else:
                    out.append('NA')

            # print(out)
            if out[0] == 'NA':
                out[0],out[1] = out[1],out[0]

            out = [','.join(x) if x != 'NA' else 'NA' for x in out]
            sys.stdout.write('%s\n'%('\t'.join(ss+out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
