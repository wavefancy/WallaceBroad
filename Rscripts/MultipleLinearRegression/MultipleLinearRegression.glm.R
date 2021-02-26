#!/usr/bin/env Rscript

"
=======================================================================================
    Do multiple linear regression, output summary statistics.
    Read data with header from stdin, and output results to stdout.
    The first column is the dependent variable.
    From second to last, are independent variables. 
    Auto generate regression formula based on data header.

Usage:
    MultipleLinearRegression.glm.R [--ci] [-r]
    MultipleLinearRegression.glm.R -h [--help]

Options:
    --ci         Output 95CI for the beta of each variable.
    -r           Output the model fit rsq.

Notes:
    1. Read data from stdin and output results to stdout.
=======================================================================================
" -> doc

# Various rsq for regression model, https://rdrr.io/cran/rsq/man/rsq.html.
# conda install -c conda-forge r-rsq
suppressMessages(library(docopt))
opts <- docopt(doc)

# if(is.null(opts$r))  TRUE else FALSE
# Binary flag do not need check is.null.
rsq  = opts$r
oci  = opts$ci

#dd = read.table("test.txt",header = T)
dd = read.table(file("stdin"),header = T)
# https://stackoverflow.com/questions/4951442/formula-with-dynamic-number-of-variables
# auto convert the colnames as formula.
form = sub('\\+','~',paste(colnames(dd), collapse = '+'))

print(c("FORMULA:",form))
# print(form)

#lr = lm(as.formula(form),data = dd)
lr = glm(as.formula(form),data = dd,family="gaussian")
summary(lr)

if(oci){
    # Calculate 95CI.
    x= confint(lr)
    y = as.data.frame(x)
    y$CI='95CI'
    y
}

if(rsq){
    suppressMessages(library(rsq))
    # ADJ = FALSE, the value is consistent with datamash ppearson
    x = rsq(lr,adj=F)
    x = formatC(x, digits = 4, format = "g") 
    cat(c('Model Rsq: ', x, '\n'),sep='\t')
}

