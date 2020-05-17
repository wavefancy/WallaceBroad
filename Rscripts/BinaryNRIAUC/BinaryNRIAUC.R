#!/usr/bin/env Rscript
# @Wallace Wang, wavefancy@gmail.com
#------------------------------

"
=======================================================================================
Net reclassification index for binary trait by logistic model.

Usage:
    BinaryNRI.R -s stdmodel -n newmdoel [-c float]
    BinaryNRI.R -h [--help]

Options:
   -s stdmodel  Standard model.
   -n newmdoel  New model.
   -c float     The cut-off for the recognization of the prediction difference of two models.
                A value of [0-1], a difference of two probabilities, default: 0.0.       

Notes:
    1. Read data from stdin and output results to stdout.
    2. Compute NRI estiamte for binary phenotye by logistic model, CI by 200 bootstrap.
    3. Compute the AUC for the two models, and test significance by Delong test. 
=======================================================================================
" -> doc

suppressMessages(library(docopt))
suppressMessages(library(data.table))
suppressMessages(library(tidyverse))
suppressMessages(library(stringr))
suppressMessages(library(pROC))
suppressMessages(library(nricens))

opts <- docopt(doc)
# print(opts)

# basemodel = eval(parse(text=opts$b))
# alternativemdoel =  eval(parse(text=opts$a))

stdmodel = opts$s
newmdoel = opts$n
cutoff   = if(is.null(opts$c)) 0.0 else {as.numerical(opts$c)}

#dd = read.table("test.txt",header = T)
dd = read.table(file("stdin"),header = T)
# remove the rows with NA values.
dd = na.omit(dd)


s = glm(as.formula(stdmodel),data = dd, family = binomial(link="logit"),x=T)
n = glm(as.formula(newmdoel),data = dd, family = binomial(link="logit"),x=T)

summary(s)
summary(n)
## Calculation of risk difference NRI
## predicted risk
# https://rdrr.io/cran/nricens/man/nricens-package.html
res = nribin(mdl.std = s, mdl.new = n, cut = cutoff, niter = 200,
       updown = 'diff')
out = rownames_to_column(res$nri)
z = res$nri[,1]/res$nri[,2]
pvalue2sided=2*pnorm(-abs(z))
out$Pvalue = pvalue2sided
cat('--------------------------\n')
write.table(format(out, digits=4),'',quote=F,row.names=F)

# Compare the AUC improvement of two models.
# https://rpubs.com/Wangzf/pROC
p.std = predict(s,type=c("response"))
p.new = predict(n,type=c("response"))

pheno = str_trim(unlist(strsplit(opts$s,'~'))[1])
rocs = roc(dd[[pheno]], p.std)
rocn = roc(dd[[pheno]], p.new)
roc_res = roc.test(rocs, rocn, method='delong')

out = data.frame(
    AUC_std = roc_res$estimate[1], AUC_new=roc_res$estimate[2],
    Pvalue = format.pval(roc_res$p.value,digits=3)
)
cat('--------------------------\n')
write.table(format(out, digits=4),'',quote=F,row.names=F, col.names=T)
