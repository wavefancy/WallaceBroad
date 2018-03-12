from hail import *
from docopt import docopt
import sys

docs='''

    Compute vcf sample QC metrics by hail sample_qc.

    Usage:
        vcfSamplesQC -i <vcf> -o <outprefix>
        vcfSamplesQC -h | --help | -v | --version

    Options:
        -i <vcf>       Test args.
        -o <outprefix> Output prefix for sample QC summary statistics, tab seq txt file.
        -h --help      Show this screen.
        -v --version   Show version.
'''

args = docopt(docs, version='0.1')

vcf=args['-i']
outprefix = args['-o']

hc = HailContext()
sys.stderr.write('>>>>Great! Load args and hail system successfully, start working!\n')

#start computing from here.
if vcf.endswith('.gz'):
    vdata = hc.import_vcf(vcf,force=True) #load for bgzip format.
else:
    vdata = hc.import_vcf(vcf)
vdata = vdata.sample_qc()
df = vdata.samples_table().to_pandas()
df.to_csv(outprefix + '.txt', sep='\t',index=False,na_rep='NA')
