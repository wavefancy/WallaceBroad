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
    ggScattterPlot.R -x name -y name -o <filename> -W float -H float [-c name ] [--sp txt] [--ylim nums] [--xlim nums] [--cp colors] [-l txt] [--lt text] [--cl txts] [--lfs num] [-s nums] [-a nums] [--xlab text] [--ylab text] [--rx int] [--xb nums] [--xl txts] [--gl] [--gls int] [--ab nums] [--abc color] [--abs num] [--revx] [--gtr txts] [--gtrs num] [--logx txt] [--vl nums] [--vc color] [--vs num]
    ggScattterPlot.R -h --help

Options:
   -x name       Column name for x axis.
   -y name       Column name for y axis.
   -c name       Column name for color, or a single color for all points, [#0073C1]. 
   -o <filename> Output file name, in pdf format. eg. example.pdf
   -W float      The width of the output figure.
   -H float      The height of the output figure.
   --sp name     Colomn name for point shapes, or a single number for R point shapes, [19].
   --cp colors   A list of color for color palette, eg. #00AFBB::#E7B800::#FC4E07.
   -l txt        Set the position for legend, default: right, c(“top”, “bottom”, “left”, “right”, “none”).
                    or vector c(x, y). Their values should be between 0 and 1 (not work now).
   --lt txt      Set the legend title as 'txt', default ['noshow']. 'noshow' to hidden.
   --lfs num     Set the legend font size, [11].
   --cl txts     Custom the order of legend elements, 
                    the text and total number of elements should match with the input, eg. 'B::C::A'.
   -s nums       Set the point size, [2].
   -a nums       Set the point alpha, [1].
   --xlim nums   Set the xlim, num1,num2
   --ylim nums   Set the ylim, num1,mum2
   --xlab text   Set x axis label, ['-x']
   --ylab text   Set y axis label, ['-y']
   --gl          Add lines for the scatter plot, by 'geom_line', aes color by '-c'
   --gls int     Set the geom_line size, [1].
   --rx int      Rotate the x axis label of degree 'int'.
   --xb nums     Set the breaks for x axis.
   --xl txts     Set the x labels for breaks, [--xb]. 
   --ab nums     Add abline (horizontal) to the plot, format: intercept,slop. eg. 0,1
   --abc color   Set the color of the abline, ['red'].
   --abs num     Set the the size for the abline, [1.5].
   --vl nums     Add vertical lines to the plot.
   --vc color    Set the color of the vertical lines, ['orange'].
   --vs num      Set the the size for the vertical lines, [1.5].
   --logx txt    Set up the log tranformation of X axis, log2|log10|sqrt.
   --revx        Reverse the X axis.
   --gtr txts    Add text to plot by 'geom_text_repel',TSV,in as: filename::col_x::col_y::col_text.
   --gtrs num    Set the text size for the gtr texts,[4].


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
suppressMessages(library(ggpubr))
suppressMessages(library(ggrepel))
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

ab   = if(is.null(opts$ab))  NULL else {as.numeric(unlist(strsplit(opts$ab,',')))}
abc  = if(is.null(opts$abc)) 'red' else {opts$abc}
abs  = if(is.null(opts$abs)) 1.5 else {as.numeric(opts$abs)}

c  = if(is.null(opts$c)) '#0073C1' else {opts$c}
sp  = if(is.null(opts$sp)) 19 else {opts$sp}

cp = if(is.null(opts$cp)) 'jco' else {unlist(strsplit(opts$cp,'::'))}
# Custom the order of legend.
cl = if(is.null(opts$cl)) NULL else {unlist(strsplit(opts$cl,'::'))}
legend = if(is.null(opts$l)) 'right' else {opts$l}
if(startsWith(legend,'c(')){
    legend = eval(parse(text=legend))
}

legendTitle = if(is.null(opts$lt)) 'noshow' else opts$lt
lfs = if(is.null(opts$lfs)) 11 else as.numeric(opts$lfs)

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
logx  = if(is.null(opts$logx)) "identity" else opts$logx
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

W = as.numeric(opts$W)
H = as.numeric(opts$H)

dd = read.table(file("stdin"),header = T, sep="\t",check.names = F)
message(paste0(colnames(dd),sep="\t"))

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

#add abline horizontal line
if(is.null(ab) == F ){
    p = p+ geom_abline(intercept = ab[1], slope = ab[2], color=abc, 
                      linetype="dashed", size=abs)
}

# add vertical lines.
# https://www.statology.org/ggplot2-vertical-line/#:~:text=You%20can%20quickly%20add%20vertical%20lines%20to%20ggplot2,xintercept%3A%20Location%20to%20add%20line%20on%20the%20x-intercept.
# xintercept, one or multiple values.
# geom_vline(xintercept, linetype, color, size)
vl_values   = if(is.null(opts$vl))  NULL else {as.numeric(unlist(strsplit(opts$vl,',')))}
vc  = if(is.null(opts$vc)) 'orange' else {opts$vc}
vs  = if(is.null(opts$vs)) 1.5 else {as.numeric(opts$vs)}
#add vertical line
if(is.null(vl_values) == F ){
    p = p+ geom_vline(xintercept=vl_values, linetype='dashed', color=vc, size=vs)
}

# https://mran.microsoft.com/snapshot/2017-08-20/web/packages/ggrepel/vignettes/ggrepel.html
# https://www.rdocumentation.org/packages/ggrepel/versions/0.8.2/topics/geom_label_repel
if(is.null(opts$gtr) == F){
    gtr = unlist(strsplit(opts$gtr,'::'))
    # data for text
    text_dd = read.table(gtr[1],header = T, sep="\t",check.names = F)

    gtrs  = if(is.null(opts$gtrs)) 4 else {as.numeric(opts$gtrs)}
    sy = 1.0
    if(is.null(opts$sy) == F){sy = as.numeric(opts$sy)}
    p = p + geom_text_repel(mapping = aes_string(gtr[2],gtr[3],label=gtr[4])
          ,data = text_dd
          ,size=gtrs,fontface='italic'
          ,nudge_y = sy
          #,nudge_x=sy
          ,segment.size = 0.5 # shift on Y, and the line size is 0.5.
          ,direction='both' # try to make no overalp on the X direction.
          ,min.segment.length = 0.5
          #,point.padding = 1.6
        )
}


p = p + ggpubr::color_palette(cp)
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

# Define the order of legends, https://rpkgs.datanovia.com/ggpubr/reference/get_palette.html
# https://ggplot2.tidyverse.org/reference/scale_manual.html
if(is.null(cl) == F){p = p + scale_color_manual(breaks = cl,values=get_palette(cp, length(cl)),labels=cl)}

# add box
p = p + border() 

ggsave(ofile, width = W, height = H)
# graphics.off()
