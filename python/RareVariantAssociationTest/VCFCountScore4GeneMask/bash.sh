# Test the capture of indels. Tested filter including VQSRTrancheSNP99.60to99.80.
# Will output [W::vcf_parse] FILTER 'VQSRTrancheSNP99.60to99.80' is not defined in the header
# But the output is right, correctly parsed the vcf.
wecho "
    python3 VCFCountScore4GeneMask.py
        -g ./test.group.txt
        -v ./test.indels.missing.vcf.gz
        --weight maf
        --max-maf 1
        --maf-bin 0.3,0.5
        -s ./samples.txt
    | bgzip > out.test.txt.gz
"
# Test the -k keep option, supass the maf filterring.
wecho "
    python3 VCFCountScore4GeneMask.py
        -g ./test.group.txt
        -v ./test.indels.missing.vcf.gz
        --weight maf
        --max-maf 0.1
        --maf-bin 0.1
        -k <(echo -e '20:1234590:G:GTC\n20:14370:G:A')
        -s ./samples.txt
    | bgzip > out.keep.txt.gz
"
wecho "
    python3 VCFCountScore4GeneMask.py
        -g ./j.group.LOFHC.gene.txt
        -v ./hg19.gene.ANGPTL8.vcf.gz
        --weight file
        --max-maf 1
        --maf-bin 0.01,1
        --mac-bin 1,3,5
        -s <(bgzip -dc ./ped.CAD.ped.gz | wcut -t IND_ID | tail -n +2)
    | bgzip > out.ANGPTL8.txt.gz
"
