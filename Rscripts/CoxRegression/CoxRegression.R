#!/usr/bin/env Rscript
# @Wallace Wang, wavefancy@gmail.com
#------------------------------

"
=======================================================================================
Cox regression model.

Usage:
    CoxRegression.R -f formula [--boot int] [-n int]
    CoxRegression.R -h [--help]

Options:
   -f formula   Formula to run the cox model.
   --boot int   Bootstrapping the input 'int' times, and do Cox model in each time.
   -n int       Set the number of threads to use when bootstrapping, [3].

Notes:
    1. Read data from stdin and output results to stdout.

Examples:
    Rscript ./CoxRegression.R -f 'Surv(time, status) ~ age + sex + ph.ecog' --boot 3
=======================================================================================
" -> doc

suppressMessages(library(docopt))
suppressMessages(library(data.table))
suppressMessages(library(tidyverse))
suppressMessages(library(stringr))
suppressMessages(library(survival))
# Version: >= furrr-0.2.1
suppressMessages(library(furrr))
# Set the output width as 10000, no breaking of the lines in linux.
options(width=10000)

opts <- docopt(doc)
# print(opts)

# basemodel = eval(parse(text=opts$b))
# alternativemdoel =  eval(parse(text=opts$a))

model   = opts$f
bootn   = if(is.null(opts$boot)) 0 else {as.integer(opts$boot)}
ncpu    = if(is.null(opts$n))    3 else {as.integer(opts$n)}

# Extract the header for all the colomns need to use in the model.
temp  = model %>% str_remove(.,'Surv') %>% str_remove_all(.,'\\(') %>% 
        str_remove_all(.,'\\)') %>% str_replace_all(.,'~','+') %>%
        str_replace_all(.,',','+')

cols  = temp %>% strsplit(.,'\\+') %>% unlist %>% str_trim

#dd = read.table("test.txt",header = T)
dd = read.table(file("stdin"),header = T)
# only keep those columns we need to use.
dd = dd[,cols]
# remove the rows with NA values.
dd = na.omit(dd)

if (bootn == 0){
    mycox <-(coxph(as.formula(model),data=dd))
    summary(mycox)
}else{
    # bootstrapping the analysis 'bootn' times.
    plan(multicore, workers =ncpu)
    results = future_map_chr(1:bootn, 
        function(x){
            set.seed(x)
            newdata = sample_n(dd, size=nrow(dd),replace = T)
            mycox <-(coxph(as.formula(model),data=newdata))
            print(summary(mycox))
            cat('-----------------------------\n')
            'DONE'
        # https://www.r-bloggers.com/2020/09/future-1-19-1-making-sure-proper-random-numbers-are-produced-in-parallel-processing/
        },.options = furrr_options(seed = TRUE))
    #print(results)
}

