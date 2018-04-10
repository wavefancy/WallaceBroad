#
# Covert gene names between different annotations.
# @Wallace Wang, wavefancy@gmail.com
# --------------------------------
# Dependent packages.
# source("https://bioconductor.org/biocLite.R")
# biocLite("org.Hs.eg.db")
# source("https://bioconductor.org/biocLite.R")
# biocLite("clusterProfiler")
# install.packages('docopt')
#
# Ref: https://bioconductor.org/packages/3.7/bioc/vignettes/clusterProfiler/inst/doc/clusterProfiler.html
'
=======================================================================================
Convert genename between different annotations.

Usage:
    GenenameConverter.R -f <from> -t <to>
    GenenameConverter.R -h [--help]

Options:
 -f   <from>     fromType, one type from supported types, eg. UNIPROT.
 -t   <to>       toType, one or more types from supported types, eg. SYMBOL,ENSEMBL.

Notes:
    1. Read one column data from stdin as input ids, no title line.
    2. Output results to stdout.
    3. Failed records will be omited from stdout. May have 1 to many mapping.
    4. Supported converting types:
        ACCNUM, ALIAS, ENSEMBL, ENSEMBLPROT, ENSEMBLTRANS, ENTREZID, ENZYME,
        EVIDENCE, EVIDENCEALL, GENENAME, GO, GOALL, IPI, MAP, OMIM, ONTOLOGY,
        ONTOLOGYALL, PATH, PFAM, PMID, PROSITE, REFSEQ, SYMBOL, UCSCKG, UNIGENE, UNIPROT

' -> doc

# load the docopt library
library(docopt)
# retrieve the command-line arguments
opts <- docopt(doc)
# what are the options? Note that stripped versions of the parameters are added to the returned list
# str(opts)
from = unlist(opts['from'][[1]])
to = strsplit(opts['to'][[1]],',')
to = c(from, unlist(to))

library(clusterProfiler)
library(org.Hs.eg.db)

dd = read.table(file("stdin"),header = F)
# ids <- bitr(dd[,1], fromType="SYMBOL", toType=c("UNIPROT", "ENSEMBL","ENTREZID","GENENAME"), OrgDb="org.Hs.eg.db")
ids <- bitr(dd[,1], fromType=from, toType=to, OrgDb="org.Hs.eg.db")
write.table(ids, stdout(), quote=F, row.names=F, col.names=T,sep='\t')
