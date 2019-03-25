#!/usr/bin/env python3

"""

    Coordinate gene name between gene list A and B. Check gene g from B refering gene
    list A. If g not in A, check if the the alias of g in A.

    @Author: wavefancy@gmail.com

    Usage:
        CooridnateGenenameAlias.py -a file -i file
        CooridnateGenenameAlias.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from B list from stdin, and output results to stdout.
            B list file: one column each line for one gene.

    Options:
        -a file       Gene list of panel A, one column, one line per gene.
        -i file       Gene info file, read the 3rd and 5th column for gene Symbol and Synonyms.
                        Example:
                            #tax_id GeneID  Symbol  LocusTag        Synonyms
                            9606    1       A1BG    -       A1B|ABG|GAB|HYST2477

                        # Download file from:
                        ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz
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
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    # reading gene_info file.
    gene_info_dic = {}
    with open(args['-i'], 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                ss = line.split()
                genes = ss[4].split('|')
                genes.append(ss[2])
                genes = set([x.upper() for x in genes if x != '-'])

                t_genes = set([x for x in genes])
                for g in genes:
                    if g in gene_info_dic:
                        # merge the list.
                        [t_genes.add(x) for x in gene_info_dic[g]]
                        # update the list for all
                        for x in gene_info_dic[g]:
                            gene_info_dic[x] = t_genes

                for g in genes:
                    gene_info_dic[g] = t_genes

    # print(gene_info_dic)

    # Read gene gene list A.
    panel_a = set()
    with open(args['-a'],'r') as f:
        for line in f:
            line = line.strip()
            if line:
                panel_a.add(line.upper())

    for line in sys.stdin:
        line = line.strip()
        if line:
            line = line.upper()
            out = [line]
            if line in panel_a:
                out.append('OK')
                out.append(line)
            else:
                ckg = [x for x in gene_info_dic.get(line, []) if x in panel_a]
                if len(ckg) == 1:
                    out.append('ALIASIN')
                    out.append(ckg[0])
                elif len(ckg) == 0:
                    out.append('SYMBOL_OR_ALIAS_NOT_IN')
                    out.append('NA')
                else:
                    out.append('NOT_UNIQUE')
                    out.append('_'.join(ckg))

            sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
