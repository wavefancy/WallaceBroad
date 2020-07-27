# @Wallace Wang, wavefancy@gmail.com
# --------------------------------
# Ref: 
# http://www.sthda.com/english/articles/32-r-graphics-essentials/132-plot-grouped-data-box-plot-bar-plot-and-more/#dot-plots

"
=======================================================================================
Create dot/bar plot with error bar using ggplot2

Usage:
    ggBarDotErrorBar.R -x name -y name (--bar|--dot) [--ymin name --ymax name] -o <filename> -W float -H float [-c name ] [--ylim nums] [--xlim nums] [--xb nums] [--xl txts] [--cp colors] [-l txt] [--lt text] [--lfs num] [--es num] [--ew num] [--ds num] [--js num] [--logy text] [--logx text] [--xlab text] [--ylabe text | --ylab text] [--yticks nums] [--ec name] [--sy] [--cl txts] [--xo txts] [--rx int]
    ggBarDotErrorBar.R -h --help

Options:
   -x name       Column name for x axis.
   -y name       Column name for y axis.
   --bar         Generate a bar plot.
   --dot         Generate a dot plot.
   --ymin name   Column name for error bar min.
   --ymax name   Column name for error bar max.
   --xlab text   Set x axis label, ['-x']
   --ylab text   Set y axis label, ['-y'].
   --ylabe text  Set y axis label, ['-y'], interpreted as expression, for supporting format.
   --yticks nums Set y axis tick positions and labels, eg. 2::5::10.
   --xb nums     Set the breaks for x axis, deimiter as ::.
   --xl txts     Set the x labels for breaks, [--xb], deimiter as ::. '-n' as line breaker. 
   -c name       Column name for color, or a single color for all points, [#0073C1].
   --ec name     Set the error bar as a single color, default as '-c'. 
   --cp colors   A list of color for color palette, eg. #00AFBB::#E7B800::#FC4E07.
   -l txt        Set the position for legend, default: right, c(“top”, “bottom”, “left”, “right”, “none”).
                    or vector c(x, y). Their values should be between 0 and 1 (not work now).
   --lt txt      Set the legend title as 'txt', default 'noshow'. 'noshow' to hidden.
   --lfs num     Set the legend font size, [11].
   --cl txts     Custom the order of legend elements, 
                    the text and total number of elements should match with the input, eg. 'B::C::A'.
   --xo txts     Custom the order on the X axis if input as factor, [in alphabet], eg. 'B::C::A'.
   --ylim nums   Set the ylim, num1,mum2
   --xlim nums   Set the xlim, num1,mum2
   --es num      Set the error bar line size, [1].
   --ew num      Set the error bar horizontal line width, [0].
   --ds num      Set the dot size, [3].
   --js num      Set the jitter size for within group elements, [0.3].
   --logy text   Set up the log tranformation of Y axis, log2|log10|sqrt.
   --logx text   Set up the log tranformation of X axis, log2|log10|sqrt.
   --rx int      Rotate the x axis label of degree 'int'.
   --sy          Show the Y value on the plot.
   -o <filename> Output file name, in pdf format. eg. example.pdf
   -W float      The width of the output figure.
   -H float      The height of the output figure.

Notes:
    1. Read data from stdin, input are 'CSV'.
    2. Output results to file.
=======================================================================================
" -> doc

# load the docopt library
options(warn=-1)
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
xlim = if(is.null(opts$xlim)) NULL else as.numeric(unlist(strsplit(opts$xlim,',')))
ylim = if(is.null(opts$ylim)) NULL else as.numeric(unlist(strsplit(opts$ylim,',')))
xticks  = waiver() # function to use the default values.
xbreaks = waiver()
addline_format <- function(x,...){
    gsub('_n','\n',x)
}
if(is.null(opts$xb) == F){
  xbreaks = as.numeric(unlist(strsplit(opts$xb,'::')))
  xticks = xbreaks
}
if(is.null(opts$xl) == F){
  xticks = unlist(strsplit(opts$xl,'::'))
  xticks = addline_format(xticks)
}
logx  = if(is.null(opts$logy)) "identity" else opts$logx
yticks = "waiver()" # function to use the default values.
if(is.null(opts$yticks) == F){
  yticks = "as.numeric(unlist(strsplit(opts$yticks,'::')))"
}
logy  = if(is.null(opts$logy)) "identity" else opts$logy

ymin = if(is.null(opts$ymin)) NULL else opts$ymin
ymax = if(is.null(opts$ymax)) NULL else opts$ymax

# Set parameters for the bar plot.
es  = if(is.null(opts$es)) 1 else as.numeric(opts$es)
ew  = if(is.null(opts$ew)) 0 else as.numeric(opts$ew)
ds  = if(is.null(opts$ds)) 3 else as.numeric(opts$ds)
js  = if(is.null(opts$js)) 0.3 else as.numeric(opts$js)


# Column for color
c  = if(is.null(opts$c)) '#0073C1' else {opts$c}
# Set colors for color palette.
cp = if(is.null(opts$cp)) NULL else {unlist(strsplit(opts$cp,'::'))}
# Set a single color for error bar.
ec = if(is.null(opts$ec)) NULL else opts$ec

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


# p  = ggplot(dd, aes_string(x,y)) +
# p  = p + geom_point(aes_string(color = c),size=ds, position = position_dodge(js))

if(opts$dot){
    p  = ggplot(dd, aes_string(x,y))
    p  = p + geom_point(aes_string(color = c),size=ds, position = position_dodge(js))
}

# Convert x and c as factor.
dd[[c]] = factor(dd[[c]])
dd[[x]] = factor(dd[[x]])

# https://rstudio-pubs-static.s3.amazonaws.com/7433_4537ea5073dc4162950abb715f513469.html
# Custom the order of legend.
cl = if(is.null(opts$cl)) NULL else {unlist(strsplit(opts$cl,'::'))}
# Order the factor the order we want.
if(is.null(cl)==F) {dd[[c]] = factor(dd[[c]], levels = cl)}
# Set the x axis item order.
xo = if(is.null(opts$xo)) NULL else {unlist(strsplit(opts$xo,'::'))}

# https://rpkgs.datanovia.com/ggpubr/reference/ggbarplot.html
if(opts$bar){
    dd[[y]] = as.numeric(unlist(dd[y]))
    p = ggbarplot(dd, x = x, y = y, 
            color = c, 
            fill=c,
            order=xo,
            position = position_dodge(js))
}

# Different ways for setting up error bar color.
if(is.null(ymin)==F && is.null(ymax)==F){
    # Force these columns to number, otherwise will have error.
    dd[[ymax]] = as.numeric(unlist(dd[ymax]))
    dd[[ymin]] = as.numeric(unlist(dd[ymin]))
    if(is.null(ec)){
        p = p + geom_errorbar(
                aes_string(ymin = ymin, ymax = ymax, color = c),
                position = position_dodge(js), width = ew, size = es
            )
        }else{
            p = p + geom_errorbar(
                    aes_string(ymin = ymin, ymax = ymax, group = c),
                    color=ec,
                    position = position_dodge(js), width = ew, size = es
                )
    }
}

# Add text to the plot.
# https://ggplot2.tidyverse.org/reference/geom_text.html
if(opts$sy){
    p = p + geom_text(aes_string(label = y, group=c), position = position_dodge(js), 
        #fontface='bold', 
        vjust=-0.25)
}

# Set the X and Y label.
myxlab = if(is.null(opts$xlab)) NULL else opts$xlab
myylabe = if(is.null(opts$ylabe)) NULL else opts$ylabe # in expression format.
myylab = if(is.null(opts$ylab)) NULL else opts$ylab
if(is.null(myxlab) == F){ p = p + xlab(myxlab)}
if(is.null(myylab) == F){ p = p + ylab(myylab)}
if(is.null(myylabe) == F){ p = p + ylab(parse(text=myylabe))}

cp = if(is.null(opts$cp)) 'jco' else {unlist(strsplit(opts$cp,'::'))}
# ggpar works, cp can be a color name or an array of colors.
p = ggpar(p, palette = cp )

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
if(class(dd[[x]]) != 'factor'){
    p = p + scale_x_continuous(trans=logx, breaks=xbreaks,labels=xticks,limits=xlim)
}
if(is.null(opts$rx) == F){p = p + rotate_x_text(as.numeric(opts$rx))}

# margin(t = 0, r = 0, b = 0, l = 0, unit = "pt")
# https://ggplot2.tidyverse.org/reference/element.html
p = p + theme(plot.margin = margin(4, 8, 4, 4, "points"))

# add box
p = p + border() 
ggsave(ofile, width = W, height = H)
# graphics.off()
