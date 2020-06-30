#
# Create grouped bar plot using ggplot2

# @Wallace Wang, wavefancy@gmail.com
# --------------------------------
# Dependent packages.
# install.packages('docopt')
#
# Ref: http://www.sthda.com/english/articles/32-r-graphics-essentials/132-plot-grouped-data-box-plot-bar-plot-and-more/

"
=======================================================================================
Create grouped bar plot using ggplot2

Usage:
    ggGroupBarPlot.R -x xname -y yname -g gname -o <filename> -W float -H float [--ymin iname --ymax aname] [--ylim nums]
    ggGroupBarPlot.R -h --help

Options:
   -x xname      Variable name for group.
   -y yname      Y values for the bar.
   -g gname      Subgroup names with in '-x', will colour differently by '-g'.
   --ymin iname   The min value for error bar.
   --ymax aname   The max value for error bar.
   --ylim nums   Set the ylim, num1,mum2
   -o <filename> Output file name, in pdf format. eg. example.pdf
   -W float      The width of the output figure.
   -H float      The height of the output figure.

Notes:
    1. Read data from stdin
    2. Output results to file.
=======================================================================================
" -> doc

# load the docopt library
options(warn=-1)
suppressMessages(library(docopt))
suppressMessages(library(ggplot2))
suppressMessages(library(tidyverse))
# suppressMessages(library(rio))
# retrieve the command-line arguments
opts <- docopt(doc)
# what are the options? Note that stripped versions of the parameters are added to the returned list
# str(opts)
# str(opts$g)
ofile = opts$o
ymin = NA
ymax = NA
if(is.null(opts$ymin) == F){
  ymin = opts$ymin
}
if(is.null(opts$ymax) == F){
  ymax = opts$ymax
}

x = opts$x
y = opts$y
g = opts$g
W = as.numeric(opts$W)
H = as.numeric(opts$H)

ylim = c()
if(is.null(opts$ylim) == F){
  ylim = as.numeric(unlist(strsplit(opts$ylim,',')))
}

dd = read.table(file("stdin"),header = T,sep="\t")

# pdf(ofile,width=W, height=H)

# mapping promatically.
# https://ggplot2.tidyverse.org/reference/aes_.html

p <- ggplot(dd, aes_string(x = x, y = y)) +
  geom_bar(
    aes_string(color = g, fill = g),
    stat = "identity", position = position_dodge(0.8),
    width = 0.7
  )
p = p + scale_color_manual(values = c("#0073C2FF", "#EFC000FF"))
p = p + scale_fill_manual(values = c("#0073C2FF", "#EFC000FF"))
# p = p + ggpubr::color_palette("jco")
p = p + ggpubr::theme_pubclean()
if(!is.na(ymin)){
  p = p + geom_errorbar(aes_string(color = g, ymin = ymin, ymax = ymax), position = position_dodge(0.8), width = 0.2)
}
# for barplot, do not use ylim.
# Use https://stackoverflow.com/questions/5936112/rescaling-the-y-axis-in-bar-plot-causes-bars-to-disappear-r-ggplot2
if(length(ylim) > 0){p = p + coord_cartesian(ylim = ylim)}
ggsave(ofile, width = W, height = H)
# graphics.off()
