# @Wallace Wang, wavefancy@gmail.com
# --------------------------------
# Ref: 
# https://ggplot2.tidyverse.org/reference/geom_boxplot.html

"
=======================================================================================
Create boxplot using ggplot2

Usage:
    ggBoxBeeswarm.R -x name -y name -o <filename> -W float -H float [-c name ] [--ylim nums] [--xlim nums] [--xb nums] [--xl txts] [--cp colors] [-l txt] [--lt text] [--lfs num] [--logy text] [--logx text] [--xlab text] [--ylabe text | --ylab text] [--yticks nums] [--cl txts] [--xo txts] [--wl num]
    ggBoxBeeswarm.R -h --help

Options:
   -x name       Column name for x axis.
   -y name       Column name for y axis.
   -o <filename> Output file name, in pdf format. eg. example.pdf
   -W float      The width of the output figure.
   -H float      The height of the output figure.
   -c name       Column name for color.
   --xlab text   Set x axis label, ['-x'].
   --ylab text   Set y axis label, ['-y'].
   --ylabe text  Set y axis label, ['-y'], interpreted as expression, for supporting format.
   --yticks nums Set y axis tick positions and labels, eg. 2::5::10.
   --xb nums     Set the breaks for x axis, deimiter as ::.
   --xl txts     Set the x labels for breaks, [--xb], deimiter as ::. '-n' as line breaker. 
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
   --logy text   Set up the log tranformation of Y axis, log2|log10|sqrt.
   --logx text   Set up the log tranformation of X axis, log2|log10|sqrt.
   
   --wl num      Set the lenght of whiskers as 'num'*IQR, [1.5].

Notes:
    1. Read data from stdin, input are 'CSV'.
    2. Output results to file.
=======================================================================================
" -> doc

options(warn=-1)
suppressMessages(library(docopt))
suppressMessages(library(ggplot2))
suppressMessages(library(tidyverse))
suppressMessages(library(ggpubr))

# conda install -c conda-forge r-ggbeeswarm r-gghalves
suppressMessages(library(gghalves))
suppressMessages(library(ggbeeswarm))

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

# Column for color
c  = if(is.null(opts$c)) NULL else {opts$c}
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

# https://rstudio-pubs-static.s3.amazonaws.com/7433_4537ea5073dc4162950abb715f513469.html
# Custom the order of legend.
cl = if(is.null(opts$cl)) NULL else {unlist(strsplit(opts$cl,'::'))}
# Order the factor the order we want.
if(is.null(cl)==F) {dd[[c]] = factor(dd[[c]], levels = cl)}
# Set the x axis item order.
xo = if(is.null(opts$xo)) NULL else {unlist(strsplit(opts$xo,'::'))}

#==============START PROJECT SPECIFIC CODE====================
### Check the columns.
incol = c(x,y,c)
incol = incol[is.null(incol)==F]
notfound = incol[incol %in% colnames(dd)==F]
if(length(notfound) > 0){
    cat("Column not found:\n", file = stderr())
    cat(notfound, file = stderr())
    cat("\n", file = stderr())
    quit(status=-1)
}

dd[[x]] = as.factor(dd[[x]])
dd[[c]] = as.factor(dd[[c]])
# Order the factor the order we want.
if(is.null(xo)==F) {dd[[x]] = factor(dd[[x]], levels = xo)}
wl = if(is.null(opts$wl)) 1.5 else as.numeric(opts$wl)

if(x!=c){ # Each group has subgroups, currently only support two.
    p = ggplot(dd, aes_string(x = x, y = y, fill=c, color=c))
    p = p + geom_boxplot(
          ,color='black'
          ,width = 0.5
          # set NA to hidden outliers.
          ,outlier.color = NA
          # The distance between box, https://ggplot2.tidyverse.org/reference/position_dodge.html
          ,position = position_dodge2(padding = 0.2)) 
      # geom_half_dotplot(method="dotdensity", stackdir="up",dotsize=0.8)
    p = p + geom_beeswarm(aes_string(x = x, y = y, fill=c, color=c)
        ,beeswarmArgs=list(side=1)
        ,size=0.9
        # the distance between groups.
        ,dodge.width=1.25)
}else{
    mynudge = 0.14
    p = ggplot(dd, aes_string(x = x, y = y, fill=c, color=c))
    p = p + geom_boxplot(
          ,color='black'
          ,width = 0.4
          # set NA to hidden outliers.
          ,outlier.color = NA
          # The shift on axis
          ,position = position_nudge(x = -1 * mynudge)) 
    # p = p + geom_beeswarm(aes_string(x = x, y = y, fill=c, color=c)
    # https://www.rdocumentation.org/packages/gghalves/versions/0.1.0/topics/geom_half_dotplot
    p = p + geom_half_dotplot(aes_string(x = x, y = y, fill=c, color=c)
        ,dotsize=0.8
        # The shift on axis
        ,position = position_nudge(x = mynudge))
}


#==============END PROJECT SPECIFIC CODE====================

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
# print('here2')
# margin(t = 0, r = 0, b = 0, l = 0, unit = "pt")
# https://ggplot2.tidyverse.org/reference/element.html
p = p + theme(plot.margin = margin(4, 8, 4, 4, "points"))

# print('here3')
# add box
p = p + border() 
ggsave(ofile, width = W, height = H)
# graphics.off()
