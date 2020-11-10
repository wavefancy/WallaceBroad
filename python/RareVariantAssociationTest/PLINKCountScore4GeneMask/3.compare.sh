# Compare the results for the ANGPTL8.
# Ignore the first three columns, plink version only counts the validated markers
# which goes into the analysis.

wecho "
    diff <(gunzip -dc out.ANGPTL8.txt.gz| wcut -f4-) <(gunzip -dc ../VCFCountScore4GeneMask/out.ANGPTL8.txt.gz | wcut -f4-) > ./diff.ANGPTL8.txt

"
