#!/usr/bin/env python3

"""

    Parse Clinvar VCF file, output variant classification based on Mark's code base.

    @Author: wavefancy@gmail.com

    Usage:
        ClinvarVariantsClassifier.py
        ClinvarVariantsClassifier.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output results to stdout.
        2. Parse the 'INFO' field. Make classification as PATHOGENIC/BENIGN/NA(something else)

    Options:
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
import re
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''

    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    num_meta = 5 #how many meta columns will keep for each variant.
    missing = 'NA'
    header = ['GENE','EFFECT','VALUE']
    indata = False
    INFO_COL = 7 # The column for INFO.

    #include in the damaging if it has this annotation (pathogenic)
    include = ['Pathogenic','Pathogenic/Likely_pathogenic','Pathogenic/Likely_pathogenic,_risk_factor','Pathogenic,_risk_factor',
               'Pathogenic,_drug_response','Pathogenic,_other','Pathogenic,_protective','Pathogenic,_Affects','Pathogenic/Likely_pathogenic,_other',
               'Pathogenic/Likely_pathogenic,_drug_response','Pathogenic,_other,_risk_factor']

    #exclude from the 5/5 if clinvar provides this annotation
    exclude = ['Uncertain_significance','Likely_benign','Benign','Benign/Likely_benign','Benign/Likely_benign,_risk_factor',
               'Benign/Likely_benign,_other','Benign/Likely_benign,_protective','Uncertain_significance,_risk_factor',
               'Benign,_risk_factor','Uncertain_significance,_other','Benign/Likely_benign,_Affects','Benign,_other',
               'Benign/Likely_benign,_association','Benign,_association,_protective','Benign/Likely_benign,_protective,_risk_factor',
               'Benign/Likely_benign,_drug_response,_risk_factor','Likely_benign,_risk_factor','Benign/Likely_benign,_drug_response']

    #conflicting annotations (need to followup)
    conflict = ['Conflicting_interpretations_of_pathogenicity','Conflicting_interpretations_of_pathogenicity,_risk_factor',
                'Conflicting_interpretations_of_pathogenicity,_other','Conflicting_interpretations_of_pathogenicity,_association',
                'Conflicting_interpretations_of_pathogenicity,_association,_other,_risk_factor','Conflicting_interpretations_of_pathogenicity,_Affects,_association,_risk_factor',
                'Conflicting_interpretations_of_pathogenicity,_other,_risk_factor','Conflicting_interpretations_of_pathogenicity,_Affects,_other',
                'Conflicting_interpretations_of_pathogenicity,_protective','Conflicting_interpretations_of_pathogenicity,_Affects']

    #do nothing with these annotations
    nothing = ['Likely_pathogenic','not_provided','risk_factor','NONE','drug_response','other','Affects','association',
               'association','protective','Likely_pathogenic,_risk_factor','protective,_risk_factor','association,_risk_factor',
               'Likely_pathogenic,_other','Affects,_association','drug_response,_protective,_risk_factor','Affects,_risk_factor',
               'Likely_pathogenic,_association']

    conflictremove = ['Likely_benign,Uncertain_significance', 'Benign,Likely_benign,Uncertain_significance', 'Benign,Uncertain_significance']
    conflictignore = ['Likely_pathogenic,Uncertain_significance', 'Likely_pathogenic,Pathogenic,Uncertain_significance',
                      'Pathogenic,Uncertain_significance', 'Likely_benign,Pathogenic,Uncertain_significance',
                      'Benign,Likely_benign,Pathogenic', 'Benign,Likely_benign,Pathogenic,Uncertain_significance',
                      'Likely_benign,Likely_pathogenic,Uncertain_significance', 'Likely_benign,Likely_pathogenic,Pathogenic,Uncertain_significance',
                      'Benign,Likely_benign,Likely_pathogenic', 'Benign,Pathogenic,Uncertain_significance', 'Likely_benign,Likely_pathogenic,Pathogenic',
                      'Benign,Likely_benign,Likely_pathogenic,Uncertain_significance', 'Likely_benign,Pathogenic', 'Likely_benign,Likely_pathogenic',
                      'Benign,Likely_pathogenic', 'Benign,Likely_benign,Likely_pathogenic,Pathogenic,Uncertain_significance', 'Benign,Likely_pathogenic,Pathogenic',
                      'Benign,Likely_pathogenic,Uncertain_significance', 'Benign,Pathogenic', 'Benign,Likely_benign,Likely_pathogenic,Pathogenic', 'NONE',
                      'Benign,Likely_pathogenic,Pathogenic,Uncertain_significance']

    damvar = ['Pathogenic','Pathogenic/Likely_pathogenic','Pathogenic/Likely_pathogenic,_risk_factor','Pathogenic,_risk_factor',
              'Pathogenic,_drug_response','Pathogenic,_other','Pathogenic,_protective','Pathogenic,_Affects',
              'Pathogenic/Likely_pathogenic,_other','Pathogenic/Likely_pathogenic,_drug_response','Pathogenic,_other,_risk_factor',
              'Pathogenic,_protective','Pathogenic,_association,_protective']
    damvar  = set([x.upper() for x in damvar])
    exclude = set([x.upper() for x in exclude])

    for line in sys.stdin:
        line = line.strip()
        if line:
            if indata:  #Parse each variant.

                ss = line.split()
                out = ss[:num_meta]

                #clinvar['CLNSIG'] = [[y for y in x.split(';') if re.search('CLNSIG=',y)][0].split('=')[1] if len([y for y in x.split(';') if re.search('CLNSIG=',y)]) > 0 else 'NONE' for x in clinvar['INFO']]
                # Extract CLINSIG values
                CLINSIG_VAL = [[y for y in x.split(';') if re.search('CLNSIG=',y)][0].split('=')[1] if len([y for y in x.split(';') if re.search('CLNSIG=',y)]) > 0 else 'NONE' for x in [ss[INFO_COL]]]
                CLINSIG_VAL = CLINSIG_VAL[0].upper()
                # print(CLINSIG_VAL)
                #clinvar['GENEINFO'] = [[y for y in x.split(';') if re.search('GENEINFO=',y)][0].split('=')[1].split(':')[0] if len([y for y in x.split(';') if re.search('GENEINFO=',y)]) > 0 else 'NONE' for x in clinvar['INFO']]
                #Extract gene name information.
                GENEINFO_VAL = [[y for y in x.split(';') if re.search('GENEINFO=',y)][0].split('=')[1].split(':')[0] if len([y for y in x.split(';') if re.search('GENEINFO=',y)]) > 0 else 'NONE' for x in [ss[INFO_COL]]]
                GENEINFO_VAL = GENEINFO_VAL[0]
                # print(GENEINFO_VAL)

                CLASS = 'PATHOGENIC' if CLINSIG_VAL in damvar  else 'NA'
                if CLASS == 'NA':
                    CLASS = 'BENIGN'     if CLINSIG_VAL in exclude else 'NA'
                # CLASS = 'CONFLICT'   if CLINSIG_VAL in conflict else 'NA'
                # CLASS = 'IGNORE'     if CLINSIG_VAL in nothing else 'NA'

                # print(CLASS)
                # print(GENEINFO_VAL)
                out.append(GENEINFO_VAL)
                out.append(CLASS)
                out.append(CLINSIG_VAL)
                # print(out)
                sys.stdout.write('%s\n'%('\t'.join(out)))

            # elif (not header and line.startswith('##INFO=<ID=CSQ')):
                # header = line.split('Format:')[1][:-2].split('|')
            elif (line.startswith('#CHROM')):
                header = line.split()[:num_meta] + header
                sys.stdout.write('%s\n'%('\t'.join(header)))
                indata = True

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
