
gunzip -dc normed.best.covs.gz | /Users/wallace/miniconda3/envs/R/bin/Rscript ./ORTop2Rest.R -n PRS -f 'PHENO ~ G + PC1 + PC2 + PC3 + PC4 + PC5 + SEX + agevisit0' -p 0.3
