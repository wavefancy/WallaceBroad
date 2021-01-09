# The example file was taken from:
# http://www.sthda.com/english/wiki/cox-proportional-hazards-model
wecho "
    gunzip -dc survival.lung.txt.gz
    |
        /Users/minxian/Broad/Program/miniconda3/envs/forestplot/bin/Rscript
        ./CoxRegression.R  -f 'Surv(time, status) ~ age + sex + ph.ecog' --boot 3
"
