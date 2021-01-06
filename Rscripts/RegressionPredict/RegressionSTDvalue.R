#!/usr/bin/env Rscript
# @Wallace Wang, wavefancy@gmail.com
#------------------------------

"
=======================================================================================
* Regress out the covariates and then scale back by add mean to the regression residual.
* Fit the a regression model from the data of stdin based on the formula, 
and add the mean value to the the regression residual.

Usage:
    RegressionSTDvalue.R -f formula [--fam text]
    RegressionSTDvalue.R -h [--help]

Options:
   -f formula   Formula to run a regression model.
   --fam text   Link function family name for glm, [gaussian].
                    https://www.statmethods.net/advstats/glm.html

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
fam = if(is.null(opts$fam)) 'gaussian' else opts$fam
yname = opts$f  %>% strsplit(.,'~')   %>% unlist %>% str_trim
yname = yname[1]

dd      = read.table(file("stdin"),header = T,check.names=F)
# newdata = read.table(opts$n,header = T,check.names=F)
# remove the rows with NA values.
dd = na.omit(dd)

lr = glm(as.formula(form),data = dd, family=fam)
# lr = lm(as.formula(form),data = dd)

# pre_out_se = predict(lr,type=c("response"),se.fit = F,newdata = dd)
# pre_out    = interval(lr,newdata=newdata,type='response')
# Combine predict se with confidence interval.
# se = as.matrix(pre_out_se[['se.fit']],ncol=1)
# colnames(se) = c('se.fit')


# out = cbind(as.matrix(pre_out),se)
# Residual + population mean.
# dd[[yname]]
# out = (dd[[yname]] - pre_out_se) + mean(dd[[yname]])

# Direct use resid instead of two steps calculate.
out = resid(lr) + mean(dd[[yname]])
out = as.matrix(out,ncol=1)
colnames(out) = c('STD_VALUE')
write.table(format(out,digits=5),"",row.names=F,col.names=T,quote=F)
# write.table(out,"",row.names=F,col.names=T,quote=F)
