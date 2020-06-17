
# Check the ref dp, no problem.
wecho "
    diff
    <(cat test.vcf | python3 ./VCFExtractDP.py -r | wcut -f1- | tail -n +2)
    # mising was code as 0 in VCFExtractDP.py
    <(cat test.vcf | bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t[\t%AD{0}]\n' | wcut -f1- | sed 's|\.|0|g')
"
# Check the total read depth. works good in this situation.
wecho "
    diff
    <(gunzip -dc ./QC.EH_LCR_SEGDUP_GQ_DP_MRR_MISSING.chrM.vcf.gz | python3 ./VCFExtractDP.py -t | wcut -f1- | tail -n +2)
    <(gunzip -dc ./QC.EH_LCR_SEGDUP_GQ_DP_MRR_MISSING.chrM.vcf.gz
        | bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t[\t%AD]\n' | wcut -f1- | sed 's|\.|0|g'
        | ppawk.py -u --rq 'f[:4]+[sum([int(y) for y in x.split(::,::)]) for x in f[4:]]'
    )
"
