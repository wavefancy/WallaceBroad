#
# Create density plot using ggplot2

# @Wallace Wang, wavefancy@gmail.com
# --------------------------------
# Dependent packages.
# install.packages('docopt')
#
# Ref: https://rpkgs.datanovia.com/ggpubr/reference/ggdensity.html

"
=======================================================================================
Create density plot using ggplot2

Usage:
    ggDensityPlot.R -x xname -o <filename> -W float -H float [-c gname] [-p palette] [--xlim nums] [--ylim nums] [--xlab text]
    ggDensityPlot.R -h --help

Options:
   -x xname      Variable name for density plot.
   -c gname      Set the color for the distribution, can be a color name
                  eg. '#00A6B3' (default light blue).
                  or a data column name, if a data column name will have multiple
                  density lines, according to the value of the column.
   --xlim nums   Set the xlim, num1,mum2
   --ylim nums   Set the ylim, num1,mum2
   --xlab text   Set x axis label, ['-x']
   -o <filename> Output file name, in pdf format. eg. example.pdf
   -p palette    Set color palette name, default 'jco'.
   -W float      The width of the output figure.
   -H float      The height of the output figure.

Notes:
    1. Read tsv data from stdin
    2. Output results to file.
=======================================================================================
" -> doc

# load the docopt library
options(warn=-1)
suppressMessages(library(docopt))
suppressMessages(library(ggplot2))
suppressMessages(library(tidyverse))
suppressMessages(library(ggpubr))
# retrieve the command-line arguments
opts <- docopt(doc)
# what are the options? Note that stripped versions of the parameters are added to the returned list
# str(opts)
# str(opts$g)
ofile = opts$o

x = opts$x
c = '#00A6B3'
pn = "jco" # color platelet name
W = as.numeric(opts$W)
H = as.numeric(opts$H)
if(is.null(opts$c) == F){ c = opts$c }
if(is.null(opts$p) == F){ pn = opts$p }

# Set the X and Y label.
myxlab = if(is.null(opts$xlab)) NULL else opts$xlab

ylim = if (is.null(opts$ylim)) NULL else as.numeric(unlist(strsplit(opts$ylim,',')))
xlim = if (is.null(opts$xlim)) NULL else as.numeric(unlist(strsplit(opts$xlim,',')))

dd = read.table(file("stdin"),header = T,sep="\t")

# pdf(ofile,width=W, height=H)
p = ggdensity(dd, x = x,  color = c, fill = c)

# https://rpkgs.datanovia.com/ggpubr/reference/ggpar.html
p = ggpar(p, xlim = xlim, ylim = ylim)
p = ggpar(p, palette = pn )
if(is.null(myxlab) == F){ p = p + xlab(myxlab)}

# https://ggplot2.tidyverse.org/reference/element.html
p = p + theme(plot.margin = margin(4, 8, 4, 4, "points"))
p
ggsave(ofile, width = W, height = H)
# graphics.off()
