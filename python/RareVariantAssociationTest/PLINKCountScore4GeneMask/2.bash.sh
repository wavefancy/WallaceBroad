# Test the capture of indels. Tested filter including VQSRTrancheSNP99.60to99.80.
# Will output [W::vcf_parse] FILTER 'VQSRTrancheSNP99.60to99.80' is not defined in the header
# But the output is right, correctly parsed the vcf.
wecho "
    python3 ./PLINKCountScore4GeneMask.py
        -g ./test.group.txt
        -p ./test.indels.missing
        --weight file
        --alt-frqs 0.3,0.5
        -s ./samples.txt
        --ov
        2>log.out.test.txt
    | bgzip > out.test.txt.gz
"
# Test weight variants by maf.
wecho "
    python3 ./PLINKCountScore4GeneMask.py
        -g ./test.group.txt
        -p ./test.indels.missing
        --weight maf
        --alt-frqs 0.3,0.5
        -s ./samples.txt
        --ov
        2>log.out.test.maf.txt
    | bgzip > out.test.maf.txt.gz
"
# Test the -k keep option, supass the maf filterring.
wecho "
    python3 ./PLINKCountScore4GeneMask.py
        -g ./test.group.txt
        -p ./test.indels.missing
        --weight file
        # No validate variants by af 0.1, the smallest af is 0.25 if 2 individuals.
        --alt-frqs 0.1
        -k <(echo -e '20:1234590:G:GTC\n20:14370:G:A')
        -s ./samples.txt
    | bgzip > out.keep.txt.gz
"
wecho "
    python3 ./PLINKCountScore4GeneMask.py
        -g ./j.group.LOFHC.gene.txt
        -p ./hg19.gene.ANGPTL8
        --weight file
        --alt-frqs 0.01,1
        --alt-acs 1,3,5
        -s <(bgzip -dc ./ped.CAD.ped.gz | wcut -t IND_ID | tail -n +2)
    | bgzip > out.ANGPTL8.txt.gz
"
