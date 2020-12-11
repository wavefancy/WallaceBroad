wecho "
    gunzip -dc ./scores.single.chr1-LOF_SAI_CLIN-CAD.txt.gz
    | Rscript ./RareRegressionAuto.R
        -f ./ped.CAD.ped
        -p CAD -i IND_ID
        -c 'Inferred_Gender,PC1,PC2,PC3,PC4,PC5,PC6,PC7,PC8,PC9,PC10'
    | bgzip > out.CAD.txt.gz
"
# Test for binary.
wecho "
    cat ./test.gene.txt
    | Rscript ./RareRegressionAuto.R
        -f ./test.ped.txt
        -p PHENO -i ID
        -c 'COV1,COV2'
        --dc 2 --cap1
    | bgzip > out.test.binary.txt.gz
"
# Test for continuous.
wecho "
    cat ./test.gene.txt
    | Rscript ./RareRegressionAuto.R
        -f ./test.ped.glm.txt
        -p PHENO -i ID
        -c 'COV1,COV2'
        --dc 2
    | bgzip > out.test.glm.txt.gz
"
# Check did SPA scaled the score.
# By the iris data, we can confirm that SPA didn't scale the input score [genotype score].
wecho "
    cat ./iris.score.txt
    | Rscript ./RareRegressionAuto.R
        -f ./iris.data.tsv
        -p pheno -i ID
        --dc 2
    | bgzip > out.test.scale.txt.gz
"
