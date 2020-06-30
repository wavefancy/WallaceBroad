#
# Create dot plot with error bar using ggplot2

# @Wallace Wang, wavefancy@gmail.com
# --------------------------------
# Dependent packages.
# install.packages('docopt')
#
# Ref: 
# http://www.sthda.com/english/articles/32-r-graphics-essentials/132-plot-grouped-data-box-plot-bar-plot-and-more/#dot-plots

"
=======================================================================================
Create dot plot with error bar using ggplot2

Usage:
    ggDotErrorBar.R -x name -y name --ymin name --ymax name -o <filename> -W float -H float [-c name ] [--ylim nums] [--cp colors] [-l txt] [--lt text] [--lfs num] [--es num] [--ew num] [--ds num] [--js num] [--logy text] [--xlab text] [--ylab text] [--yticks nums]
    ggDotErrorBar.R -h --help

Options:
   -x name       Column name for x axis.
   -y name       Column name for y axis.
   --ymin name   Column name for error bar min.
   --ymax name   Column name for error bar max.
   --xlab text   Set x axis label, ['-x']
   --ylab text   Set y axis label, ['-y']
   --yticks nums Set y axis tick positions and labels, eg. 2,5,10.
   -c name       Column name for color, or a single color for all points, [#0073C1]. 
   --cp colors   A list of color for color palette, eg. #00AFBB::#E7B800::#FC4E07.
   -l txt        Set the position for legend, default: right, c(“top”, “bottom”, “left”, “right”, “none”).
                    or vector c(x, y). Their values should be between 0 and 1 (not work now).
   --lt txt      Set the legend title as 'txt', default 'noshow'. 'noshow' to hidden.
   --lfs num     Set the legend font size, [11].
   --ylim nums   Set the ylim, num1,mum2
   --es num      Set the error bar line size, [1].
   --ew num      Set the error bar horizontal line width, [0].
   --ds num      Set the dot size, [3].
   --js num      Set the jitter size for within group elements, [0.3].
   --logy text   Set up the log tranformation of Y axis, log2|log10|sqrt.
   -o <filename> Output file name, in pdf format. eg. example.pdf
   -W float      The width of the output figure.
   -H float      The height of the output figure.

Notes:
    1. Read data from stdin, input are 'CSV'.
    2. Output results to file.
=======================================================================================
" -> doc

# load the docopt library
suppressMessages(library(docopt))
suppressMessages(library(ggplot2))
suppressMessages(library(tidyverse))
suppressMessages(library(ggpubr))
# suppressMessages(library(rio))
# retrieve the command-line arguments
opts <- docopt(doc)
# what are the options? Note that stripped versions of the parameters are added to the returned list
# str(opts)
# str(opts$g)
ofile = opts$o

# Column for x, y, and set x, y lim.
x = opts$x
y = opts$y
xlim = c()
ylim = NULL
if(is.null(opts$ylim) == F){
  ylim = as.numeric(unlist(strsplit(opts$ylim,',')))
}
ymin = opts$ymin
ymax = opts$ymax
yticks = "waiver()" # function to use the default values.
if(is.null(opts$yticks) == F){
  yticks = "as.numeric(unlist(strsplit(opts$yticks,',')))"
}

# Set the X and Y label.
myxlab = if(is.null(opts$xlab)) NULL else opts$xlab
myylab = if(is.null(opts$ylab)) NULL else opts$ylab

# Set parameters for the bar plot.
es  = if(is.null(opts$es)) 1 else as.numeric(opts$es)
ew  = if(is.null(opts$ew)) 0 else as.numeric(opts$ew)
ds  = if(is.null(opts$ds)) 3 else as.numeric(opts$ds)
js  = if(is.null(opts$js)) 0.3 else as.numeric(opts$js)
logy  = if(is.null(opts$logy)) "identity" else opts$logy

# Column for color
c  = if(is.null(opts$c)) '#0073C1' else {opts$c}
# Set colors for color palette.
cp = if(is.null(opts$cp)) NULL else {unlist(strsplit(opts$cp,'::'))}

# Set legend.
legend = if(is.null(opts$l)) 'right' else {opts$l}
if(startsWith(legend,'c(')){
    legend = eval(parse(text=legend))
}
legendTitle = if(is.null(opts$lt)) 'noshow' else opts$lt
lfs = if(is.null(opts$lfs)) 11 else as.numeric(opts$lfs)

# Set figure width and height.
W = as.numeric(opts$W)
H = as.numeric(opts$H)

# dd = read.table(file("stdin"),header = T,sep="\t")
dd = read.csv(file("stdin"),check.names=F)
cat(colnames(dd), file = stderr())
cat("\n", file = stderr())

# pdf(ofile,width=W, height=H)
# Force these columns to number, otherwise will have error.
dd[[ymax]] = as.numeric(unlist(dd[ymax]))
dd[[ymin]] = as.numeric(unlist(dd[ymin]))
p  = ggplot(dd, aes_string(x,y)) +
        geom_errorbar(
            aes_string(ymin = ymin, ymax = ymax, color = c),
            position = position_dodge(js), width = ew, size = es
        )
p  = p + geom_point(aes_string(color = c),size=ds, position = position_dodge(js))

# Set the X and Y label.
if(is.null(myxlab) == F){ p = p + xlab(myxlab)}
if(is.null(myylab) == F){ p = p + ylab(myylab)}

if(is.null(cp)){
    p = p + ggpubr::color_palette("jco")
}else{
    p = p + ggpubr::color_palette(cp)
}
if(length(xlim) > 0){p = p + xlim(xlim[1],xlim[2])}
# if(length(ylim) > 0){p = p + ylim(ylim[1],ylim[2])}


# Change theme things.
p = p + theme_pubr()
# https://rpkgs.datanovia.com/ggpubr/reference/ggpar.html
p = ggpar(p,legend=legend, legend.title = legendTitle)
# change the font size for legend.
p = ggpar(p,font.legend = lfs)
# no show legend title. 
# more about legend. https://www.datanovia.com/en/blog/ggplot-legend-title-position-and-labels/
# set the size as 0 is better than set theme(legend.title = element_blank()).
if (legendTitle == 'noshow') {p = p + theme(legend.title = element_text(size=0))}
# Note: the command legend.justification sets the corner that the position refers to.
# https://www.r-graph-gallery.com/239-custom-layout-legend-ggplot2.html
if (length(legend) == 2){ p = p + theme(legend.justification = c("left", "top"))}
# https://ggplot2.tidyverse.org/reference/scale_continuous.html
p = p + scale_y_continuous(trans=logy, breaks=eval(parse(text=yticks)),labels=eval(parse(text=yticks)),limits=ylim)

# https://rpkgs.datanovia.com/ggpubr/reference/ggpar.html
# if (logy != '') {p = ggpar(p,yscale=logy)}
# p = ggpar(p,yticks.by=1)

# margin(t = 0, r = 0, b = 0, l = 0, unit = "pt")
# https://ggplot2.tidyverse.org/reference/element.html
p = p + theme(plot.margin = margin(4, 8, 4, 4, "points"))

# add box
p = p + border() 
p
ggsave(ofile, width = W, height = H)
# graphics.off()
