
wecho "
    zcat /seq/dax/Kathiresan_MiGenExS/Exome/v11/Kathiresan_MiGenExS.vcf.gz
    | wcut -c --cs '##' -f1-20 | vcftools --vcf - -c --recode --max-missing 0.95 --maf 0.3 | head -n 250 | bgzip > test.maf0.3.vcf.gz
"
wecho "
      scp $l2s:/medpop/esp2/projects/MIGEN/v11/SampleSubset/PROMIS/test.vcf.gz ./
    !!scp $l2s:/medpop/esp2/projects/MIGEN/v11/SampleSubset/PROMIS/test.maf0.3.vcf.gz ./

"

