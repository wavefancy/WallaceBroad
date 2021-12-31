'
Feature selection by the R ExhaustiveSearch package.

Notes:
  * The GWAS summary must has the following columns:

Usage:
  FSExhaustiveSearch.R -f formula --family name -n int

Options:
  -f formula    Regression formula.
  --family name Link function family, gaussian|binomial.
  -n int        Output the top `int` number of top results.
' -> doc
# no line breaks.
options(width = 10000)
# Example for feature selection.
# https://github.com/RudolfJagdhuber/ExhaustiveSearch


# update to auto-detect and install packages.
# https://stackoverflow.com/questions/4090169/elegant-way-to-check-for-missing-packages-and-install-them
# http://trinker.github.io/pacman/vignettes/Introduction_to_pacman.html
if (!require("pacman"))  install.packages("pacman")
pacman::p_load(dplyr, docopt, rio, data.table, ExhaustiveSearch,
    install = TRUE, update=FALSE)
# require and install the minimal version.
# if (p_version(bigsnpr) < '1.7.1') p_install_version(c("bigsnpr"),c("1.7.1"))

opts <- docopt(doc)
# what are the options? Note that stripped versions of the parameters are added to the returned list
# str(opts)
form  = opts$f
fam   = opts$family
outn  = opts$n
MSGE <- function(...) cat(sprintf(...), sep='', file=stderr())

dd = read.table(file("stdin"),header = T)
ES <- ExhaustiveSearch(as.formula(form), data = dd, 
        family = fam, quietly = TRUE)
print(ES)
resultTable(ES, n = outn)