#!/usr/bin/env python3

"""
    Aggregate/weight the number of rare variant for each individual in each gene.
        * A single pass can classify variant into multiple alt frequency or count bins.
        * Facilitate downstream burden based test for checking multiple conditions.
        *** format: PLINK2 pgen/psam/pvar/pvar.zst, 
        *** `do not` support multi-allelic sites. 

    Dependenciees:
        * zstandard: conda install -c anaconda zstandard
        * pgenlib  : https://github.com/chrchang/plink-ng/tree/master/2.0/Python

    @Author: wavefancy@gmail.com

    Usage:
        PgenCountScore4GeneMask.py -g file -p txt [--weight text] [-s file] [-n int] [-k file] [--alt-frqs floats] [--alt-acs ints] [--ov]
        PgenCountScore4GeneMask.py -h | --help | --version | -f | --format

    Notes:
        1. Output to stdout, each line for each gene mask.
        2. *** Do not support multi-allelic sites in the current version.
        3. *** Output individual name only use 'iid' as identifier, ignore family id 'fid'.

    Options:
        -g file          Group file, each line is a group of variants, 
                            eg. GENE1 CHR:POS:REF:ALT[:weight] CHR:POS:REF:ALT[:weight] ...
                                The weight refer to the ALT allele, scored as copy_of_alt_allele*weight.
        -p txt           File name prefix for PLINK pgen format file, pgen/psam/pvar/pvar.zst.
                                *** Varinat ID should in the foramt of CHR:POS:REF:ALT.
        --weight txt     The way for aggregate variant. Default: file.
                             file: sum(alt_count*variant_weight), variant_weight from group file.
                                   Set as 1 if group file don't have weight.
                             maf:  Set the weight as 1/(MAF*(1-MAF))^0.5. Madsen and Browning (2009).
        -s file          Sample file, only count the score for those individuals decleared in this file.
        -n int           [Not yet ready] Set the number of threads, Default 2, usually no impove as more threads.
        --alt-frqs floats Allele frequency cut-off for alt allele, eg. 0.01|0.01,0.05.
                                For a single pass, the variants will be checked if meet any 'alt-frqs' cut-off,
                                IF so, will contribute to the score for each bin it met the condition.
        --alt-acs ints    Allele count cut-off for alt allele, eg. 5|1,3.
                                For a single pass, the variants will be checked if meet any 'alt-acs' cut-off,
                                IF so, will contribute to the score for each bin it met the condition.
        -k file          Always keep the variants listed in this file, surpass frequency and allele count filtering.
                            Put id line by line, CHR:POS:REF:ALT format.
        --ov             Output qualified variant list used in the scoring to stderr.
        -h --help        Show this screen.
        --version        Show version.
        -f --format      Show format example.
"""
import sys
import os.path
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
from collections import OrderedDict
import numpy as np
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    ''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.1')
    # version 1.1
    # Check format at each line. FORMAT may different line by line.
    # print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    group_file = args['-g']
    plink_prefix = args['-p']
    weight_way = args['--weight'] if args['--weight'] else 'file'
    weight_way = weight_way.lower()
    if weight_way not in set(['file','maf']):
        sys.stderr.write('Please set a proper value for --weight')
    # set the number of threads, not use for now.
    N_threads = 2
    if args['-n']:
        N_threads = int(args['-n'])
        # ne.set_num_threads(N_threads)

    # Sample name to work on.
    sample_set = set()
    if args['-s']:
        with open(args['-s'], 'r') as sfile:
            for line in sfile:
                line = line.strip()
                if line:
                    ss = line.split()
                    [sample_set.add(x) for x in ss]
    # convert list to set for fast checking
    # samples = set(samples)

    # The variant list we always want to keep, no matter what's the MAF and MAC filter is.
    KeepVIDs = set()
    if args['-k']:
        with open(args['-k'], 'r') as content_file:
            content = content_file.read().strip().split()
            KeepVIDs = set(content)
    #print(KeepVIDs)

    # Will check if a varinat met any maf or mac bin.
    mafs = [float(x) for x in args['--alt-frqs'].split(',')] if args['--alt-frqs'] else []
    macs = [int(x)   for x in args['--alt-acs'].split(',')] if args['--alt-acs'] else []

    MAX_MAF = max(mafs)  if mafs else 1
    MAX_MAC = max(macs)  if macs else 9000000000
    OUT_QUALIFIED_VARIANTS  = True if args['--ov'] else False

    if len(mafs) == 0 and len(macs) == 0:
        sys.stderr.write("At least one should be open: '--alt-frqs' and/or '--alt-acs'\n")
        sys.exit(-1)
    
    # Open and work on pgen file
    # https://github.com/chrchang/plink-ng/blob/master/2.0/Python/python_api.txt
    # https://github.com/chrchang/plink-ng/blob/master/2.0/Python/single_variant_test.py

    import pgenlib
    import numpy as np

    ###### Read psam file, and idenfiy sample set need to read later on. ######
    use_samples = []
    use_samples_index = []
    N_sample_psam = -1  # No. of samples defined in psam file.
    with open(plink_prefix+'.psam','r') as psam: # only use the #IID column.
        IID_COL = -1
        for line in psam:
            ss = line.split()
            if IID_COL < 0:
                IID_COL = ss.index('#IID')
            else:
                N_sample_psam += 1 # start from 0.
                if ss[IID_COL] in sample_set:
                    use_samples.append(ss[IID_COL])
                    use_samples_index.append(N_sample_psam)
    use_samples_index = np.array(use_samples_index, np.uint32)
    # index starts from 0, so the total N need add 1.
    N_sample_psam += 1

    ###### Read in the variant list. ######
    pvar = plink_prefix + '.pvar'
    if os.path.isfile(pvar):
        pvar = open(pvar,'r', encoding="utf-8")
    elif os.path.isfile(plink_prefix+'.pvar.zst'):
        import zstandard as zstd
        import io
        zst_temp = open(plink_prefix+'.pvar.zst', 'rb')
        dctx = zstd.ZstdDecompressor()
        stream_reader = dctx.stream_reader(zst_temp)
        pvar = io.TextIOWrapper(stream_reader, encoding='utf-8')
    else:
        sys.stderr.write("ERROR, file not exist: '%s' or '%s'\n"%(plink_prefix + '.pvar', plink_prefix+'.pvar.zst'))
        sys.exit(-1)
    
    # Reading in the varinats
    VarIDIndexMap = {}
    # VarIDAltMap = {}
    IDCOL = -1
    ALTCOL = -1
    N_vars_pvar = -1 # No. of var defined in pvar file.
    for line in pvar:
        if line.startswith('##'):
            pass
        elif line.startswith('#CHROM'):
            ss = line.split()
            IDCOL = ss.index('ID')
            ALTCOL = ss.index('ALT')
        else:
            ss = line.split()
            N_vars_pvar += 1
            ID = ss[IDCOL]
            if ID in VarIDIndexMap:
                # print('here')
                pvar.close()
                sys.stderr.write('ERROR, duplicate variant ID: %s\n'%(ID))
                sys.exit(-1)
            else:
                # VarIDAltMap[ID] = ss[ALTCOL]
                if ss[ALTCOL] != ID.split(':')[3]:
                    pvar.close()
                    sys.stderr.write('ERROR, Alt allele is not matched with its codig in varinat ID: %s\n'%(line))
                    sys.exit(-1)
                VarIDIndexMap[ID] = np.uint32(N_vars_pvar)
    pvar.close()
    # N_vars_pvar, index starts from 0, so the total N need add 1.
    N_vars_pvar += 1
    # print(VarIDIndexMap)
    # print(N_vars_pvar)

    ###### Open pgen file for reading. ######
    pf =  pgenlib.PgenReader(bytes(plink_prefix + '.pgen','utf8'),
        raw_sample_ct = N_sample_psam,
        variant_ct    = N_vars_pvar,
        sample_subset = use_samples_index)
    # Buffer to load genotypes, number of alt alleles, missing as -9.
    genotypes = np.empty(len(use_samples_index), np.int8)

    ###### compute gene burden score ######
    out = "#CHROM  BEGIN   END     MARKER_ID       NUM_ALL_VARS    NUM_PASS_VARS   NUM_SING_VARS MAF/MAC_CUT".split()
    sys.stdout.write('%s\t%s\n'%('\t'.join(out), '\t'.join(use_samples)))
    N_samples = len(use_samples_index)

    # go through the group file and count the scores.
    with open(group_file, 'r') as gfile:
        for line in gfile: # Process by group file, line by line, each line is a gene.
            line = line.strip()
            # print('---------------------')
            if line: # for each gene
                ss = line.split()

                min_pos = 100000000000
                max_pos = -1
                chr = ''
                
                # record weight map
                # Load the snp list in a gene (a row), and set up the weight.
                NUM_ALL_VARS = 0  # the number of sites defined in group file, but also found in input file.
                record_weight = OrderedDict() # The weight for each snp.
                # record_alt    = OrderedDict() # The alt allele base.
                for snp in ss[1:]:
                    t = snp.split(':')
                    key = ':'.join(t[:4])
                    chr = t[0]
                    if key in VarIDIndexMap:
                        w = float(t[4]) if len(t) == 5 else 1.0
                        record_weight[key] = w
                        # record_alt[key]    = t[3].upper() # only keep at the upper case.
                        pos = int(t[1])
                        min_pos = min(min_pos,pos)
                        max_pos = max(max_pos,pos)
                        # print(max_pos)

                # results for different MAFs and MACs.
                MAF_RESULTS = OrderedDict()        # Individual scores.
                MAF_RESULTS_PASS = OrderedDict()   # Number of passed variants, met the maf/mac filtration.
                MAF_RESULTS_SING = OrderedDict()   # Number of singleton.
                MAF_QUALIFIED_SNPS = OrderedDict() # The qualified snp list in the scoring.
                MAC_RESULTS = OrderedDict()
                MAC_RESULTS_PASS = OrderedDict()
                MAC_RESULTS_SING = OrderedDict()
                MAC_QUALIFIED_SNPS = OrderedDict()

                if mafs:
                    for x in mafs:
                        MAF_RESULTS[str(x)] = np.zeros(N_samples)
                        MAF_RESULTS_PASS[str(x)] = 0
                        MAF_RESULTS_SING[str(x)] = 0
                        MAF_QUALIFIED_SNPS[str(x)] = []
                if macs:
                    for x in macs:
                        MAC_RESULTS[str(x)] = np.zeros(N_samples)
                        MAC_RESULTS_PASS[str(x)] = 0
                        MAC_RESULTS_SING[str(x)] = 0
                        MAC_QUALIFIED_SNPS[str(x)] = []

                # Goes for marker one by one.
                for marker_id in record_weight.keys():
                    # The genotypes was coded as the number of alt allele.
                    # -9 as missing values.
                    # np array, int8.
   
                    # Load the alt count to the buffer of genotypes. np array, int8
                    pf.read(VarIDIndexMap[marker_id],genotypes)
                    # Impute the missing(-9) to the ref allele
                    genotypes[genotypes<0] = 0

                    NUM_ALL_VARS += 1
                    alt_count = np.sum(genotypes)      # Total number of alt alleles.
                    aaf = alt_count/(2.0*N_samples) # alt allele frequency across samples.
                    # v_maf = min(aaf, 1-aaf)
                    v_maf = aaf
                    v_mac = alt_count

                    if v_mac == 0: continue # I don't think this kind of sites make sense for testing.
                    weight = np.power(1/(aaf * (1-aaf)),0.5) if weight_way == 'maf' else record_weight[marker_id]

                    # Fake the maf(mac) as 0, to pass the maf filtering, in order to always keep this variant.
                    if KeepVIDs and (marker_id in KeepVIDs):
                        v_maf = 0.0
                        v_mac = 0
                    if v_maf > MAX_MAF and v_mac > MAX_MAC: #max-maf or max-mac filtering.
                        continue

                    genos = genotypes * weight

                    # filter by maf and do computation:
                    if v_maf <= MAX_MAF and mafs:
                        # aggregate results
                        for maf in mafs:
                            if v_maf <= maf:
                                aid = str(maf)
                                MAF_RESULTS_PASS[aid] = MAF_RESULTS_PASS[aid] + 1
                                # t = MAF_RESULTS[aid]
                                MAF_RESULTS[aid] = MAF_RESULTS[aid] + genos
                                # sys.stderr.write('IN::%s\t%s\t%s\t%s\n'%(id,str(v_maf),str(v_mac),aid))
                                if OUT_QUALIFIED_VARIANTS:
                                    MAF_QUALIFIED_SNPS[aid].append(marker_id)

                                if alt_count == 1:
                                    MAF_RESULTS_SING[aid] = MAF_RESULTS_SING[aid] + 1
                                # print("AF: %s\t%s\n"%(aid,marker_id))

                    # filter by mac and do computation:
                    if v_mac <= MAX_MAC and macs:
                        # aggregate results
                        for mac in macs:
                            if v_mac <= mac:
                                aid = str(mac)
                                MAC_RESULTS_PASS[aid] = MAC_RESULTS_PASS[aid] + 1
                                # t = MAC_RESULTS[aid]
                                MAC_RESULTS[aid] = MAC_RESULTS[aid] + genos
                                if OUT_QUALIFIED_VARIANTS:
                                    MAC_QUALIFIED_SNPS[aid].append(id)

                                if alt_count == 1:
                                    MAC_RESULTS_SING[aid] = MAC_RESULTS_SING[aid] + 1
                                # print("AC: %s\t%s\n"%(aid,marker_id))

                
                out = [chr, str(min_pos),str(max_pos),ss[0]]
                # print(MAF_RESULTS)
                #output results
                for maf in mafs:
                    aid = str(maf)
                    myout = out + [str(NUM_ALL_VARS), str(MAF_RESULTS_PASS[aid]), str(MAF_RESULTS_SING[aid]), aid] + ['%g'%(x) for x in MAF_RESULTS[aid]]
                    sys.stdout.write('%s\n'%('\t'.join(myout)))
                    if OUT_QUALIFIED_VARIANTS:
                        eout = out + [aid, ','.join(MAF_QUALIFIED_SNPS[aid]) if MAF_QUALIFIED_SNPS[aid] else 'NA']
                        sys.stderr.write('%s\n'%('\t'.join(eout)))
                for mac in macs:
                    aid = str(mac)
                    myout = out + [str(NUM_ALL_VARS), str(MAC_RESULTS_PASS[aid]), str(MAC_RESULTS_SING[aid]), aid] + ['%g'%(x) for x in MAC_RESULTS[aid]]
                    sys.stdout.write('%s\n'%('\t'.join(myout)))
                    if OUT_QUALIFIED_VARIANTS:
                        eout = out + [aid, ','.join(MAC_QUALIFIED_SNPS[aid]) if MAC_QUALIFIED_SNPS[aid] else 'NA']
                        sys.stderr.write('%s\n'%('\t'.join(eout)))

    pf.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
