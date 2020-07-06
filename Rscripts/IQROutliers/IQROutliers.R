#!/usr/bin/env Rscript
# @Wallace Wang, wavefancy@gmail.com
#------------------------------

# IQR rule and implementation details:
# 1. https://www.khanacademy.org/math/statistics-probability/summarizing-quantitative-data/box-whisker-plots/a/identifying-outliers-iqr-rule
# 2. https://stackoverflow.com/questions/12866189/calculating-the-outliers-in-r
"
=======================================================================================
Detect outliers based on 1.5xIQR rule.

    A commonly used rule says that a data point is an outlier 
    if it is more than 1.5⋅IQR above the third quartile 
    or below the first quartile. Said differently, low outliers 
    are below Q1−1.5⋅IQR and high outliers are above Q3+1.5⋅IQR.

Usage:
    IQROutliers.R -n name [-t num]
    IQROutliers.R -h [--help]

Options:
   -n name   Column name for checking outliers.
   -t num    Set the IQR threshold for declearing outliers, [1.5].

Notes:
    1. Read tsv data from stdin and output results to stdout.
    2. Input should without missing data for column '-n.'
=======================================================================================
" -> doc
options(warn=-1)
suppressMessages(library(docopt))

opts <- docopt(doc)
threshold = if(is.null(opts$t)) 1.5 else {as.numeric(opts$t)}

# define a function to remove outliers
FindOutliers <- function(data) {
  lowerq = quantile(data)[2]
  upperq = quantile(data)[4]
  iqr = upperq - lowerq #Or use IQR(data)
  # we identify extreme outliers
  extreme.threshold.upper = (iqr * threshold) + upperq
  extreme.threshold.lower = lowerq - (iqr * threshold)
  result <- which(data > extreme.threshold.upper | data < extreme.threshold.lower)
}

#dd = read.table("test.txt",header = T)
dd = read.table(file("stdin"),header = T,check.names=F)
out = FindOutliers(dd[[opts$n]])

write.table(dd[out,] ,"",row.names=F,col.names=T,quote=F)
