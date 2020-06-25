
# Check the ref dp, no problem.
wecho "
    diff
    <(cat ../VCFDPFilter/test.vcf | python3 ./VCFExtractDP.py -r | wcut -f1- | tail -n +2)
    # mising was code as 0 in VCFExtractDP.py
    <(cat ../VCFDPFilter/test.vcf | bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t[\t%AD{0}]\n' | wcut -f1- | sed 's|\.|nan|g')
"
# Check the total read depth. works good in this situation.
# This input has some problem, however the first 100 colums are valid.
# Confirmed worked good as the bcftools.
wecho "
    diff
    <(gunzip -dc ../VCFDPFilter/QC.EH_LCR_SEGDUP_GQ_DP_MRR_MISSING.chrM.vcf.gz | wcut -f1-100 -c --cs '##' | python3 ./VCFExtractDP.py -t | wcut -f1- | tail -n +2 | sed 's|nan|0|g')
    <(gunzip -dc ../VCFDPFilter/QC.EH_LCR_SEGDUP_GQ_DP_MRR_MISSING.chrM.vcf.gz | wcut -f1-100 -c --cs '##'
        | bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t[\t%AD]\n' | wcut -f1- | sed 's|\.|0|g'
        | ppawk.py -u --rq 'f[:4]+[sum([int(y) for y in x.split(::,::)]) for x in f[4:]]'
    )
"
# Compare the extract the DP field.
wecho "
    diff
    <(gunzip -dc ../VCFDPFilter/QC.EH_LCR_SEGDUP_GQ_DP_MRR_MISSING.chrM.vcf.gz | wcut -f1-100 -c --cs '##' | python3 ./VCFExtractDP.py -d | wcut -f1- | tail -n +2 | sed 's|nan|0|g')
    <(gunzip -dc ../VCFDPFilter/QC.EH_LCR_SEGDUP_GQ_DP_MRR_MISSING.chrM.vcf.gz | wcut -f1-100 -c --cs '##'
        | bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t[\t%DP]\n' | wcut -f1- | sed 's|\.|0|g'
    )
"
