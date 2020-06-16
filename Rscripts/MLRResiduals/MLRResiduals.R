#!/usr/bin/env Rscript
# @Wallace Wang, wavefancy@gmail.com
#------------------------------

"
=======================================================================================
Compute the residual from a multiple linear regression.

Usage:
    MLRResiduals.R -f formula
    MLRResiduals.R -h [--help]

Options:
   -f formula   Formula to run the cox model.

Notes:
    1. Read data from stdin and output results to stdout.
    2. Rows with NA will be auto removed, no show in the output.
    3. Add on more column with header as 'RESIDUALS'.
=======================================================================================
" -> doc

suppressMessages(library(docopt))
suppressMessages(library(data.table))
suppressMessages(library(tidyverse))
suppressMessages(library(stringr))

opts <- docopt(doc)
# print(opts)

form   = opts$f

#dd = read.table("test.txt",header = T)
dd = read.table(file("stdin"),header = T,check.names=F)
# remove the rows with NA values.
dd = na.omit(dd)

lr = lm(as.formula(form),data = dd)
dd$RESIDUALS = resid(lr)
write.table(dd ,"",row.names=F,col.names=T,quote=F)
