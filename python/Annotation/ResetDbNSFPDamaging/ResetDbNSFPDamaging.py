#!/usr/bin/env python3

"""

    Reset dnNSFP damaging annotion.

    @Author: wavefancy@gmail.com

    Usage:
        ResetDbNSFPDamaging.py
        ResetDbNSFPDamaging.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. If any transcript annotion has damaging prediction, set as D else N.
        3. Currently only support the reset of
            'SIFT_pred Polyphen2_HDIV_pred Polyphen2_HVAR_pred LRT_pred MutationTaster_pred MutationAssessor_pred MetaSVM_pred MetaLR_pred M-CAP_pred PROVEAN_pred FATHMM_pred'.

    Options:
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)
import codecs
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'UTF-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
if sys.stdin.encoding  != 'UTF-8':
    sys.stdin = codecs.getreader('utf-8')(sys.stdin.buffer, 'strict')

def ShowFormat():
    '''Input File format example:'''
    print('''
    ''')

# dbNSFP 3.5a ReadMe, variant classification
# https://drive.google.com/file/d/0B60wROKy6OqcNGJ2STJlMTJONk0/view

# .       40391751        0.268060
#D       63232977        0.419646
#T       47056885        0.312293
# SIFT_pred: If SIFTori is smaller than 0.05 (rankscore>0.395) the corresponding nsSNV is
#		predicted as "D(amaging)"; otherwise it is predicted as "T(olerated)".
#		Multiple predictions separated by ";"

#.       11027847        0.102315
#B       34489731        0.319991
#D       39291666        0.364542
#P       22974338        0.213152
# Polyphen2_HDIV_pred: Polyphen2 prediction based on HumDiv, "D" ("probably damaging",
#		HDIV score in [0.957,1] or rankscore in [0.52844,0.89865]), "P" ("possibly damaging",
#		HDIV score in [0.453,0.956] or rankscore in [0.34282,0.52689]) and "B" ("benign",
#		HDIV score in [0,0.452] or rankscore in [0.02634,0.34268]). Score cutoff for binary
#		classification is 0.5 for HDIV score or 0.3528 for rankscore, i.e. the prediction is
#		"neutral" if the HDIV score is smaller than 0.5 (rankscore is smaller than 0.3528),
#		and "deleterious" if the HDIV score is larger than 0.5 (rankscore is larger than
#		0.3528). Multiple entries are separated by ";".

#.       11027847        0.102084
#B       42428265        0.392754
#D       31698431        0.293429
#P       22873087        0.211734
# Polyphen2_HVAR_pred: Polyphen2 prediction based on HumVar, "D" ("probably damaging",
#		HVAR score in [0.909,1] or rankscore in [0.62797,0.97092]), "P" ("possibly damaging",
#		HVAR in [0.447,0.908] or rankscore in [0.44195,0.62727]) and "B" ("benign", HVAR
#		score in [0,0.446] or rankscore in [0.01257,0.44151]). Score cutoff for binary
#		classification is 0.5 for HVAR score or 0.45833 for rankscore, i.e. the prediction
#		is "neutral" if the HVAR score is smaller than 0.5 (rankscore is smaller than
#		0.45833), and "deleterious" if the HVAR score is larger than 0.5 (rankscore is larger
#		than 0.45833). Multiple entries are separated by ";".

#.       16107458        0.193407
#D       36818886        0.442094
#N       25582396        0.307175
#U       4774119 0.057324
# LRT_pred: LRT prediction, D(eleterious), N(eutral) or U(nknown), which is not solely
#		determined by the score.

# .       2246141 0.009169
#A       8707555 0.035546
#D       156000864       0.636828
#N       77834460        0.317736
#P       176452  0.000720
# MutationTaster_pred: MutationTaster prediction, "A" ("disease_causing_automatic"),
#		"D" ("disease_causing"), "N" ("polymorphism") or "P" ("polymorphism_automatic"). The
#		score cutoff between "D" and "N" is 0.5 for MTnew and 0.31713 for the rankscore.

# MetaSVM_pred
#.       7519568 0.083907
#D       13663364        0.152463
#T       68434853        0.763630

#M-CAP_pred
#.       11583101        0.129250
#D       40128069        0.447769
#T       37906615        0.422981

#MetaLR_pred
#.       7519568 0.083907
#D       14557286        0.162437
#T       67540931        0.753655

#MutationAssessor_pred
#.       20158730        0.224941
#H       4895251 0.054624
#L       22645922        0.252695
#M       28229553        0.314999
#N       13688329        0.152741
# MutationAssessor_pred: MutationAssessor's functional impact of a variant :
#		predicted functional, i.e. high ("H") or medium ("M"), or predicted non-functional,
#		i.e. low ("L") or neutral ("N"). The MAori score cutoffs between "H" and "M",
#		"M" and "L", and "L" and "N", are 3.5, 1.935 and 0.8, respectively. The rankscore cutoffs
#		between "H" and "M", "M" and "L", and "L" and "N", are 0.92922, 0.51944 and 0.19719,
#		respectively.

# Mark's damaging mask.
#Scores used for 'of five' designations:
#SIFT_pred Polyphen2_HDIV_pred Polyphen2_HVAR_pred LRT_pred MutationTaster_pred
#SIFT_Pred: D/P/H/M/A; D = Damaging
#Polyphen2_HDIV: D/P/H/M/A; D= Probably damaging; P= Possible damaging
#Polyphen2_HVAR: D/P/H/M/A; D= Probably damaging; P= Possible damaging
#LRT_Pred: D=Deleterious
#MutationTaster_pred: D/A; A=DiseaseCausingAutomatic; D=DiseaseCausing

if __name__ == '__main__':
    args = docopt(__doc__, version='2.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    #classification map for the five predictions.
    # M-CAP_pred PROVEAN_pred FATHMM_pred
    CLASS_MAP={
        "SIFT_pred".upper()          : set(['D']),
        "Polyphen2_HDIV_pred".upper(): set(['D','P']),
        "Polyphen2_HVAR_pred".upper(): set(['D','P']),
        "LRT_pred".upper()           : set(['D']),
        "MutationTaster_pred".upper(): set(['A','D']),
        "MutationAssessor_pred".upper(): set(['H','M']), # 37%
        "MetaSVM_pred".upper(): set(['D']), # 15%
        "MetaLR_pred".upper(): set(['D']), # 16%
        "M-CAP_pred".upper(): set(['D']), # 44%
        "PROVEAN_pred".upper(): set(['D']),
        "FATHMM_pred".upper(): set(['D'])
    }

    title = False
    COL_INDEX = {}
    for line in sys.stdin:
        line = line.strip()
        if line:
            line = line.replace(';','&') # transcript level prediction separated by ';' from dbNSFP.
            ss = line.split()
            if title:
                ss = line.split()
                # Reset the classification label.
                for k in COL_INDEX.keys():
                    pred = ss[COL_INDEX[k]].upper().split('&') # get transcript level predictions.
                    dam = [x for x in pred if x in CLASS_MAP[k]] # any transcript is damaging, treat as damaging.
                    if dam:
                        ss[COL_INDEX[k]] = 'D'
                    else:
                        ss[COL_INDEX[k]] = 'N'
            else:
                title = True
                for i, k in enumerate([x.upper() for x in ss]):
                    if k in CLASS_MAP:
                        COL_INDEX[k] = i

            sys.stdout.write('%s\n'%('\t'.join(ss)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
