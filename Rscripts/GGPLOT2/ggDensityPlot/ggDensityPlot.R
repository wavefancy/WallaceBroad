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
    ggDensityPlot.R -x xname -o <filename> -W float -H float [-c gname] [--cp colors] [--xlim nums] [--ylim nums] [--xlab text] [-l txt] [--lt txt] [--lfs num]
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
   --cp colors   A list of color for color palette, eg. #00AFBB::#E7B800::#FC4E07 or a single for palette name, [jco].
   -l txt        Set the position for legend, default: right, c(“top”, “bottom”, “left”, “right”, “none”).
                    or vector c(x, y). Their values should be between 0 and 1 (not work now).
   --lt txt      Set the legend title as 'txt', 'noshow' to hidden, [noshow].
   --lfs num     Set the legend font size, [11].
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
W = as.numeric(opts$W)
H = as.numeric(opts$H)
if(is.null(opts$c) == F){ c = opts$c }
cp = if(is.null(opts$cp)) 'jco' else {unlist(strsplit(opts$cp,'::'))}

legend = if(is.null(opts$l)) 'right' else {opts$l}
if(startsWith(legend,'c(')){
    legend = eval(parse(text=legend))
}
legendTitle = if(is.null(opts$lt)) 'noshow' else opts$lt
lfs = if(is.null(opts$lfs)) 11 else as.numeric(opts$lfs)

# Set the X and Y label.
myxlab = if(is.null(opts$xlab)) NULL else opts$xlab

ylim = if (is.null(opts$ylim)) NULL else as.numeric(unlist(strsplit(opts$ylim,',')))
xlim = if (is.null(opts$xlim)) NULL else as.numeric(unlist(strsplit(opts$xlim,',')))

dd = read.table(file("stdin"),header = T,sep="\t")

# pdf(ofile,width=W, height=H)
p = ggdensity(dd, x = x,  color = c, fill = c,
        legend.title = legendTitle,
    )

# Change theme things.
p = p + theme_pubr(legend=legend)
# change the font size for legend.
p = ggpar(p,font.legend = lfs)
# no show legend title. 
# more about legend. https://www.datanovia.com/en/blog/ggplot-legend-title-position-and-labels/
# set the size as 0 is better than set theme(legend.title = element_blank()).
if (legendTitle == 'noshow') {p = p + theme(legend.title = element_text(size=0))}
# Note: the command legend.justification sets the corner that the position refers to.
# https://www.r-graph-gallery.com/239-custom-layout-legend-ggplot2.html
if (length(legend) == 2){ p = p + theme(legend.justification = c("left", "top"))}


# https://rpkgs.datanovia.com/ggpubr/reference/ggpar.html
p = ggpar(p, xlim = xlim, ylim = ylim)
# ggpar works, cp can be a color name or an array of colors.
p = ggpar(p, palette = cp )
# p = p + ggpubr::color_palette(cp)
if(is.null(myxlab) == F){ p = p + xlab(myxlab)}

# https://ggplot2.tidyverse.org/reference/element.html
p = p + theme(plot.margin = margin(4, 8, 4, 4, "points"))
# add box
p = p + border() 
ggsave(ofile, width = W, height = H)
