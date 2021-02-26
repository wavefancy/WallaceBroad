
wecho "
      cat test.txt | /Users/minxian/Broad/Program/miniconda3/envs/forestplot2/bin/Rscript MultipleLinearRegression.R
    !!cat test.txt | /Users/minxian/Broad/Program/miniconda3/envs/forestplot2/bin/Rscript MultipleLinearRegression.glm.R

    # cat test.txt | datamash -H ppearson 1:2
    # ppearson(census)
    # 0.58244547710521*0.58244547710521 = 0.3392
    !!cat test.txt | wcut -f1,2 | /Users/minxian/Broad/Program/miniconda3/envs/forestplot2/bin/Rscript MultipleLinearRegression.glm.R -r
    # Model Rsq:      0.3392
"
