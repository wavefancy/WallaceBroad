# Compare the results for the ANGPTL8.
# Ignore the first three columns, plink version only counts the validated markers
# which goes into the analysis.

# A full compare by real data for a whole chromosome.
# The PLINK/bim version is about 40 times faster than the VCF version.
# /medpop/esp2/wallace/projects/Amit/MI_EOMI_BURDEN_AUTO/SoftwareBechmark/UKB_13K/BURDEN_TEST

wecho "
    diff <(gunzip -dc out.ANGPTL8.txt.gz) <(gunzip -dc ../PLINKCountScore4GeneMask/out.ANGPTL8.txt.gz) > ./diff.ANGPTL8.txt
"
