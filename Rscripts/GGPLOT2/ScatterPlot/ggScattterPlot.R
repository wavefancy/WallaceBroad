#
# Create scatter plot using ggplot2

# @Wallace Wang, wavefancy@gmail.com
# --------------------------------
# Dependent packages.
# install.packages('docopt')
#
# Ref: http://www.sthda.com/english/articles/24-ggpubr-publication-ready-plots/78-perfect-scatter-plots-with-correlation-and-marginal-histograms/

"
=======================================================================================
Create scatter plot using ggplot2

Usage:
    ggScattterPlot.R -x name -y name -o <filename> -W float -H float [-c name ] [--sp txt] [--ylim nums] [--xlim nums] [--cp colors] [-l txt] [--lt text] [--lfs num] [-s nums] [-a nums] [--xlab text] [--ylab text] [--rx int] [--xb nums] [--xl txts] [--gl] [--gls int]
    ggScattterPlot.R -h --help

Options:
   -x name       Column name for x axis.
   -y name       Column name for y axis.
   -c name       Column name for color, or a single color for all points, [#0073C1]. 
   --sp name     Colomn name for point shapes, or a single number for R point shapes, [19].
   --cp colors   A list of color for color palette, eg. #00AFBB::#E7B800::#FC4E07.
   -l txt        Set the position for legend, default: right, c(“top”, “bottom”, “left”, “right”, “none”).
                    or vector c(x, y). Their values should be between 0 and 1 (not work now).
   --lt txt      Set the legend title as 'txt', default by system group name. 'noshow' to hidden.
   --lfs num     Set the legend font size, [11].
   -s nums       Set the point size, [2].
   -a nums       Set the point alpha, [1].
   --xlim nums   Set the xlim, num1,num2
   --ylim nums   Set the ylim, num1,mum2
   --xlab text   Set x axis label, ['-x']
   --ylab text   Set y axis label, ['-y']
   --gl          Add lines for the scatter plot, by 'geom_line', aes color by '-c'
   --gls int     Set the geom_line size, [1].
   --rx int      Rotate the x axis label of degree 'int'.
   --xb nums    Set the breaks for x axis.
   --xl txts    Set the x labels for breaks, [--xb]. 
   -o <filename> Output file name, in pdf format. eg. example.pdf
   -W float      The width of the output figure.
   -H float      The height of the output figure.

Notes:
    1. Read data from stdin
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

x = opts$x
y = opts$y
ylim = NULL
if(is.null(opts$ylim) == F){
  ylim = as.numeric(unlist(strsplit(opts$ylim,',')))
}

c  = if(is.null(opts$c)) '#0073C1' else {opts$c}
sp  = if(is.null(opts$sp)) 19 else {opts$sp}

cp = if(is.null(opts$cp)) NULL else {unlist(strsplit(opts$cp,'::'))}
legend = if(is.null(opts$l)) 'right' else {opts$l}
if(startsWith(legend,'c(')){
    legend = eval(parse(text=legend))
}

# Set property for X axis.
rx = if(is.null(opts$rx)) NULL else {as.numeric(opts$rx)}
xticks = "waiver()" # function to use the default values.
xbreaks = "waiver()"
if(is.null(opts$xb) == F){
  xbreaks = "as.numeric(unlist(strsplit(opts$xb,',')))"
  xticks = xbreaks
}
if(is.null(opts$xl) == F){
  xticks = "unlist(strsplit(opts$xl,','))"
}
logx  = if(is.null(opts$logy)) "identity" else opts$logx
xlim = NULL
if(is.null(opts$xlim) == F){
  xlim = as.numeric(unlist(strsplit(opts$xlim,',')))
}

# Set the X and Y label.
myxlab = if(is.null(opts$xlab)) NULL else opts$xlab
myylab = if(is.null(opts$ylab)) NULL else opts$ylab

# Set for geom_line
gl = opts$gl   # directly converted to F/T by docopt.
gls = if(is.null(opts$gls)) 1 else {as.numeric(opts$gls)}

# Set the point size and alpha.
size  = if(is.null(opts$s)) 2 else {as.numeric(opts$s)}
alpha = if(is.null(opts$a)) 1 else {as.numeric(opts$a)}

legendTitle = if(is.null(opts$lt)) NULL else opts$lt
lfs = if(is.null(opts$lfs)) 11 else as.numeric(opts$lfs)

W = as.numeric(opts$W)
H = as.numeric(opts$H)

dd = read.table(file("stdin"),header = T,sep="\t",check.names = F)
message(paste0(colnames(dd),sep="\t"))

pdf(ofile,width=W, height=H)

# dd[[x]] = as.numeric(unlist(dd[x]))
# dd[[y]] = as.numeric(unlist(dd[y]))
p = ggscatter(dd, x = x, y = y, shape = sp, color = c,
        # legend=legend, legend.title = legendTitle,
        # Set legend later in theme_
        legend.title = legendTitle,
        size = size, alpha = alpha,
    )

if (gl==T){
    p = p + geom_line(aes_string(color=c),size=gls)
}

if(is.null(cp)){
    p = p + ggpubr::color_palette("jco")
}else{
    p = p + ggpubr::color_palette(cp)
}
# if(length(xlim) > 0){p = p + xlim(xlim[1],xlim[2])}
if(length(ylim) > 0){p = p + ylim(ylim[1],ylim[2])}

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
if(is.null(rx) == F){p = p + rotate_x_text(rx)}
# https://ggplot2.tidyverse.org/reference/scale_continuous.html
p = p + scale_x_continuous(trans=logx, breaks=eval(parse(text=xbreaks)),labels=eval(parse(text=xticks)),limits=xlim)
# Set the X and Y label.
if(is.null(myxlab) == F){ p = p + xlab(myxlab)}
if(is.null(myylab) == F){ p = p + ylab(myylab)}

# margin(t = 0, r = 0, b = 0, l = 0, unit = "pt")
# https://ggplot2.tidyverse.org/reference/element.html
p = p + theme(plot.margin = margin(4, 8, 4, 4, "points"))


# add box
p = p + border() 
p
graphics.off()
