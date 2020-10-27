#!/usr/bin/env Rscript
# @Wallace Wang, wavefancy@gmail.com
#------------------------------

"
=======================================================================================
Fit the a regression model from the data of stdin based on the formula, 
and predict a new value for the new data.

Usage:
    RegressionPredict.R -f formula -n file
    RegressionPredict.R -h [--help]

Options:
   -f formula   Formula to run the cox model.
   -n file      The file contain the new data to predict.

Notes:
    1. Read data from stdin and output results to stdout.
    2. Rows with NA (missing value) will be ignored.
    3. A R glm model was fit, supported 'family': https://www.statmethods.net/advstats/glm.html

Packages:
    # HH, https://rdrr.io/cran/HH/
    conda install -c conda-forge r-hh
=======================================================================================
" -> doc

suppressMessages(library(docopt))
suppressMessages(library(data.table))
suppressMessages(library(tidyverse))
suppressMessages(library(stringr))
suppressMessages(library(HH))

opts <- docopt(doc)
# print(opts)

form   = opts$f

dd      = read.table(file("stdin"),header = T,check.names=F)
newdata = read.table(opts$n,header = T,check.names=F)
# remove the rows with NA values.
dd = na.omit(dd)

lr = glm(as.formula(form),data = dd, family='gaussian')
pre_out_se = predict(lr,type=c("response"),se.fit = TRUE,newdata = newdata)
pre_out    = interval(lr,newdata=newdata,type='response')
# Combine predict se with confidence interval.
se = as.matrix(pre_out_se[['se.fit']],ncol=1)
colnames(se) = c('se.fit')

out = cbind(as.matrix(pre_out),se)
write.table(format(out,digits=5),"",row.names=F,col.names=T,quote=F)
