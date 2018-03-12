from hail import *
from docopt import docopt
import sys

docs='''

    Compute vcf sample QC metrics by hail sample_qc.

    Usage:
        vcfSamplesQC -i <vcf> -o <outprefix> [--gq]
        vcfSamplesQC -h | --help | -v | --version

    Options:
        -i <vcf>       Test args.
        -o <outprefix> Output prefix for sample QC summary statistics, tab seq txt file.
        --gq           Direct read GQ value from VCF, do not recompute from PL.
                          Hail will recompute from PL as default, which is totally bad.
        -h --help      Show this screen.
        -v --version   Show version.
'''

args = docopt(docs, version='0.1')

vcf=args['-i']
outprefix = args['-o']

hc = HailContext()
sys.stderr.write('>>>>Great! Load args and hail system successfully, start working!\n')

store_gq = True if args['--gq'] else False
#start computing from here.
if vcf.endswith('.gz'):
    vdata = hc.import_vcf(vcf,generic=False, store_gq=store_gq) #load for bgzip format.
else:
    vdata = hc.import_vcf(vcf)
vdata = vdata.sample_qc()
df = vdata.samples_table().to_pandas()
df.to_csv(outprefix + '.txt', sep='\t',index=False,na_rep='NA')
