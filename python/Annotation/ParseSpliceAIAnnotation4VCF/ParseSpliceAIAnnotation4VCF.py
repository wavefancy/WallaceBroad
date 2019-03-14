#!/usr/bin/env python3

"""

    Parse SpliceAI annotation for VCF file.

    @Author: wavefancy@gmail.com

    Usage:
        ParseSpliceAIAnnotation4VCF.py
        ParseSpliceAIAnnotation4VCF.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output results to stdout.
        2. Parse the 'SpliceAI' field, make each gene one line,
           Keeping the first 5 meta columns for each variants.

    Options:
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
# ------ INPUT ----------
##contig=<ID=GL000193.1,length=189789>
##contig=<ID=GL000194.1,length=191469>
##contig=<ID=GL000225.1,length=211173>
##contig=<ID=GL000192.1,length=547496>
##INFO=<ID=SpliceAI,Number=.,Type=String,Description="SpliceAIv1.2.1 variant annotation. These include delta scores (DS) and delta positions (DP) for acceptor gain (AG), acceptor loss (AL), donor gain (DG), and donor loss (DL). Format: ALLELE|SYMBOL|DS_AG|DS_AL|DS_DG|DS_DL|DP_AG|DP_AL|DP_DG|DP_DL">
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
1       861255  .       A       G       .       .       SpliceAI=G|SAMD11|0.01|0.02|0.01|0.00|47|23|138|23
1       861255  .       A       C       .       .       SpliceAI=C|SAMD11|0.01|0.01|0.01|0.02|23|47|87|-75
1       861261  .       G       A       .       .       SpliceAI=A|SAMD11|0.01|0.01|0.00|0.00|17|41|-116|-81
1       861265  .       C       T       .       .       SpliceAI=T|SAMD11|0.01|0.02|0.00|0.01|13|37|-85|-120,T|AL645608.1|0.00|0.01|0.00|0.00|184|437|184|305
1       861265  .       C       A       .       .       SpliceAI=A|SAMD11|0.03|0.03|0.01|0.02|37|13|128|-85,A|AL645608.1|0.00|0.00|0.00|0.00|71|437|228|281
1       861265  .       C       T       .       .       SpliceAI=T|SAMD11|0.01|0.02|0.00|0.01|13|37|-85|-120,T|AL645608.1|0.00|0.01|0.00|0.00|184|437|184|305

# ------ OUTPUT ----------
#CHROM  POS     ID  REF  ALT  ALLELE  SYMBOL      DS_AG  DS_AL  DS_DG  DS_DL  DP_AG  DP_AL  DP_DG  DP_DL
1       861255  .   A    G    G       SAMD11      0.01   0.02   0.01   0.00   47     23     138    23
1       861255  .   A    C    C       SAMD11      0.01   0.01   0.01   0.02   23     47     87     -75
1       861261  .   G    A    A       SAMD11      0.01   0.01   0.00   0.00   17     41     -116   -81
1       861265  .   C    T    T       SAMD11      0.01   0.02   0.00   0.01   13     37     -85    -120
1       861265  .   C    T    T       AL645608.1  0.00   0.01   0.00   0.00   184    437    184    305
1       861265  .   C    A    A       SAMD11      0.03   0.03   0.01   0.02   37     13     128    -85
1       861265  .   C    A    A       AL645608.1  0.00   0.00   0.00   0.00   71     437    228    281
1       861265  .   C    T    T       SAMD11      0.01   0.02   0.00   0.01   13     37     -85    -120
1       861265  .   C    T    T       AL645608.1  0.00   0.01   0.00   0.00   184    437    184    305
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    num_meta = 5 #how many meta columns will keep for each variant.
    missing = 'NA'
    header = []
    indata = False
    for line in sys.stdin:
        line = line.strip()
        if line:
            if indata:  #Parse each variant.
                # line = line.replace(' ','_')
                ss = line.split()
                out = ss[:num_meta]
                # print(ss)
                data = ss[7].split('SpliceAI=')[1].split(',')
                for d in data:
                    dout = out + d.split('|')
                    dout = [ missing if not d else d for d in dout]
                    sys.stdout.write('%s\n'%('\t'.join(dout)))

            elif (not header and line.startswith('##INFO=<ID=SpliceAI')):
                header = line.split('Format:')[1][:-2].strip().split('|')
            elif (line.startswith('#CHROM')):
                header = line.split()[:num_meta] + header
                sys.stdout.write('%s\n'%('\t'.join(header)))
                indata = True

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
