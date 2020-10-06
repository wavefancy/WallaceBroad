#
# Covert gene names between different annotations.
# @Wallace Wang, wavefancy@gmail.com
# --------------------------------
# - conda install -c bioconda bioconductor-clusterprofiler bioconductor-org.hs.eg.db bioconductor-do.db
# - conda install -c conda-forge r-docopt r-rio
# 
# - R version 3.15 or higher [IF failed by conda, try this]
# if (!requireNamespace("BiocManager", quietly = TRUE))
#    install.packages("BiocManager")
# BiocManager::install()
# BiocManager::install(c("clusterProfiler", "org.Hs.eg.db"))
# 
# --------------------------------
# - Dependent packages.
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
    ClusterProfilerEnrichKEGG.R -t file -o text [-b file] [-p value] [-q value]
    ClusterProfilerEnrichKEGG.R -h [--help]

Options:
 -t file      Gene ids ranked in the top, one gene per line. EntrezID.
 -o text      Output file name prefix.
 -b file      Background genes, if missing using all genes in database as background.
                   One gene per line. EntrezID.
 -p value     P value cutoff for the output of top enriched pathways. [0.05]
 -q value     Q value cutoff for the output of top enriched pathways. [0.2]

Notes:

' -> doc

suppressMessages(library(docopt))
# retrieve the command-line arguments
opts <- docopt(doc)
# what are the options? Note that stripped versions of the parameters are added to the returned list
# str(opts)
topG   = read.table(opts$t,header = F)
outF   = opts$o
backG  = if(is.null(opts$b)) NULL  else read.table(opts$b,header = F)
pcut   = if(is.null(opts$p)) 0.05 else as.numeric(opts$p)
qcut   = if(is.null(opts$q)) 0.2  else as.numeric(opts$q)

suppressMessages(library(clusterProfiler))
suppressMessages(library(org.Hs.eg.db))
suppressMessages(library(rio))

# Enrichment for KEGG
ego <- enrichKEGG(
            gene          = as.character(topG[,1]),
            universe      = as.character(backG[,1]),
            organism      = 'hsa',
            pAdjustMethod = "bonferroni",
            pvalueCutoff  = pcut,
            qvalueCutoff  = qcut,
)
# Convert gene ID to gene symbol.
ego = setReadable(ego, org.Hs.eg.db, keyType = "ENTREZID")
export(as.data.frame(ego), file=paste0(outF,'_KEGG','.tsv.gz'))

# Enrichment for KEGG Module
ego <- enrichMKEGG(
            gene          = as.character(topG[,1]),
            universe      = as.character(backG[,1]),
            organism      = 'hsa',
            pAdjustMethod = "bonferroni",
            pvalueCutoff  = pcut,
            qvalueCutoff  = qcut,
)
# Convert gene ID to gene symbol.
ego = setReadable(ego, org.Hs.eg.db, keyType = "ENTREZID")
export(as.data.frame(ego), file=paste0(outF,'_KEGG-Module','.tsv.gz'))


