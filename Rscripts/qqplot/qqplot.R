#
# Generate QQ plot based on input P values.
# With the ability to high light genes.

# @Wallace Wang, wavefancy@gmail.com
# --------------------------------
# Dependent packages.
# install.packages('docopt')
#
# Ref: https://bioconductor.org/packages/3.7/bioc/vignettes/clusterProfiler/inst/doc/clusterProfiler.html

"
=======================================================================================
Generate QQ plot based on input P values.

Usage:
    qqplot.R [-g <genes>] -o <filename>
    qqplot.R -h [--help]

Options:
   -g <genes>    Gene list to label in the figure. eg. gene1|gene1,gene2.
   -o <filename> Output file name, in pdf format. eg. example.pdf

Notes:
    1. Read data from stdin, with header P as pvalue,
          if '-g' is on, need one more column named as GENENAME.
    2. Output results to file.
=======================================================================================
" -> doc

# load the docopt library
suppressMessages(library(docopt))
suppressMessages(library(ggplot2))
suppressMessages(library(dplyr))
suppressMessages(library(ggrepel))
# retrieve the command-line arguments
opts <- docopt(doc)
# what are the options? Note that stripped versions of the parameters are added to the returned list
# str(opts)
# str(opts$g)
ofile = opts$o
genes = c()
if(is.null(opts$g) == F){
  genes = strsplit(opts$g,',')
  genes = unlist(genes)
}
# str(genes)

dd = read.table(file("stdin"),header = T)

# function to generate QQ plot
gg_qqplot = function(df, genes, ci=0.95) {
  xs=df$P
  N = length(xs)
  df$observed=-log10(df$P)
  df=arrange(df,desc(observed))
  df$expected=-log10(1:N / N)
  log10Pe = expression(paste("Expected -log"[10], plain(P)))
  log10Po = expression(paste("Observed -log"[10], plain(P)))
  df$Label=""
  df$Label[df$GENENAME %in% genes]=as.character(df$GENENAME[df$GENENAME %in% genes])
  thresh=thresh=log10(2.5e-6)*-1
  ggplot(df) +
    geom_abline(intercept=0, slope=1, alpha=0.5,size=2) +
    geom_point(aes(expected, observed), shape=19, alpha=0.7,size=4,color='darkblue',fill='darkblue') +
    geom_hline(yintercept=thresh,color='red',size=0.7,,linetype='dashed') +
    xlab(log10Pe) +
    ylab(log10Po)+
    geom_text_repel(aes(expected,observed,label=Label),size=6,fontface='italic',point.padding = 1.6) +
    theme_bw()+
    theme(
      text = element_text(color = "black"),
      axis.title.x = element_text(vjust = -.5,size=20,face="bold",margin = unit(c(5, 0, 0, 0),'mm'),colour = 'black'),
      axis.title.y = element_text(vjust = 1,size=20,,face="bold",margin = unit(c(0, 5, 0, 0),"mm"),colour = 'black'),
      axis.text = element_text(size=16, colour = 'black'),
      axis.ticks = element_line(colour = 'black', size = 1),
      panel.grid.major = element_line(colour="gray", size=0.5,linetype = "dotted"),
      panel.grid.minor = element_blank(),
      panel.border = element_rect(linetype = "solid", colour = "black", size=1.5),
      axis.ticks.length = unit(7, "pt"), # Change the length of tick marks
    )
}

pdf(ofile,width=5.5, height=5.5)
gg_qqplot(dd,genes)
graphics.off()
