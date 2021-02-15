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
    qqplot.R [-g <genes>] -o <filename> [-H float] [-W float] [--xlim nums] [--ylim nums] [--sy float] [--yb floats] [--ybl txts] [--tp float] [--l text]
    qqplot.R -h [--help]

Options:
   -g <genes>    Gene list to label in the figure. eg. gene1|gene1::gene2.
   -H float      Set the HEIGHT for the plot figure, [5.5].
   -W float      Set the WIDTH  for the plot figure, [5.5].
   --xlim nums   Set the xlim, num1::num2
   --ylim nums   Set the ylim, num1::mum2
   --yb floats   Set the tick breaks for Y axis, eg. 1,2,3,4.
   --ybl txts    Set the tick texts for Y axis,  eg. a,b,c,d.
   --sy float    The distance for shift on the Y axis, default 0.5.
   --tp float    Horizontal line threshold for significance, [noshow]. 
   --l text      Add inflation lambda to the plot, format: X::Y::Value.
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
suppressMessages(library(tidyverse))
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
xlim = c()
ylim = c()
if(is.null(opts$xlim) == F){
  xlim = as.numeric(unlist(strsplit(opts$xlim,',')))
}
if(is.null(opts$ylim) == F){
  ylim = as.numeric(unlist(strsplit(opts$ylim,',')))
}
sy = 0.5
if(is.null(opts$sy) == F){sy = as.numeric(opts$sy)}
# The breaks for Y label.
yb = c()
if(is.null(opts$yb) == F){
  yb = as.numeric(unlist(strsplit(opts$yb,',')))
}
ybl = c()
if(is.null(opts$ybl) == F){
  ybl = as.numeric(unlist(strsplit(opts$ybl,',')))
}
lambda = if(is.null(opts$l)==F) unlist(strsplit(opts$l,'::')) else NULL
pwidth  = if(is.null(opts$W)==F) as.numeric(opts$W) else 5.5
pheight = if(is.null(opts$H)==F) as.numeric(opts$H) else 5.5

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
  # thresh=log10(2.5e-6)*-1
  gg = ggplot(df) +
    geom_abline(intercept=0, slope=1, alpha=0.5,size=2) +
    geom_point(aes(expected, observed), shape=19, alpha=0.7,size=4,color='darkblue') +
    # geom_point(aes(expected, observed), shape=21, alpha=0.7,size=4,color='black') +
    # add the horizontal line.
    # geom_hline(yintercept=thresh,color='red',size=0.7,,linetype='dashed') +
    xlab(log10Pe) +
    ylab(log10Po)+
    geom_text_repel(aes(expected,observed,label=Label),size=5,fontface='italic'
      ,nudge_y = sy,segment.size = 0.5 # shift on Y, and the line size is 0.5.
      ,direction='x' # try to make no overalp on the X direction.
      #,point.padding = 1.6
    ) +
    theme_bw()+
    theme(
      text = element_text(color = "black"),
      # margin as top, right, bottom,left.
      axis.title.x = element_text(vjust = -.5,size=14,face="bold",margin = unit(c(1, 0, 0, 0),'mm'),colour = 'black'),
      axis.title.y = element_text(vjust = 1,size=14,,face="bold",margin = unit(c(0, 1, 0, 0),"mm"),colour = 'black'),
      axis.text = element_text(size=12, colour = 'black'),
      axis.ticks = element_line(colour = 'black', size = 1),
      # panel.grid.major = element_line(colour="gray", size=0.5,linetype = "dotted"),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      panel.border = element_rect(linetype = "solid", colour = "black", size=1.5),
      axis.ticks.length = unit(7, "pt"), # Change the length of tick marks
    )
  # add horizontal dashed line, default no show.
  if(is.null(opts$tp) == F){
      thresh = log10(as.numeric(opts$tp))*-1.0
      gg = gg + geom_hline(yintercept=thresh,color='red',size=0.7,,linetype='dashed')
  }

  # add lambda values.
  if(is.null(lambda)==F){
    # math annotation in R
    # https://stat.ethz.ch/R-manual/R-devel/library/grDevices/html/plotmath.html
    # style italic not work here.
    gg = gg + geom_text(x=as.numeric(lambda[1]), y=as.numeric(lambda[2]), label=paste('italic(lambda ==',lambda[3],')'),fontface='italic', parse=T,size=5)
  }
  
  # make highlight of the label.
  red = df %>% filter(Label != "")
  if(dim(red)[1] > 0) {gg = gg + geom_point(data=red,aes(x=expected,y=observed), colour='#C21B90',size=4)}
  if(length(xlim) > 0){gg = gg + xlim(xlim[1],xlim[2])}
  # if(length(ylim) > 0){gg = gg + ylim(ylim[1],ylim[2])}
  if(length(yb)>0){
    gg = gg + scale_y_continuous(
    breaks = yb,
    label =  ybl,
    limits = ylim)
  }else{
    if(length(ylim) > 0){gg = gg + ylim(ylim[1],ylim[2])}
  }
  
  gg
}

pdf(ofile,width=pwidth, height=pheight)
gg_qqplot(dd,genes)
graphics.off()
