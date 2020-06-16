'
Generate Forest Plot by the Publish package.

Notes:
  * Read data from stdin and output results to files.
  * The "OR,OR_CI_L,OR_CI_R" are required 3 colums, for OR and ORCI.
  * All the other colums are copied and to show on the plot.
  * INPUT format are tsv file.

Usage:
  ForestPlot.R -o <filename> -W float -H float [-g name] [-x xlabel] [--xlim nums] [--xr xratio]

Options:
  -o <filename> Output file name, in pdf format. eg. example.pdf
  -W float      The width of the output figure.
  -H float      The height of the output figure.
  -g name       Split the input by "name", plot each susbset by a section.
  -x xlabel     Set the X label name, default "Log(Odds Ratio)".
  --xr xratio   Set the ratio of text panel, default 0.8.
  --xlim nums   Set the xlim, num1,num2

  ' -> doc

# Generate Forest plot.
# Worked version : Publish_2019.12.04 prodlim_2018.04.18
suppressMessages(library(Publish))
suppressMessages(library(tidyverse))
suppressMessages(library(docopt))
suppressMessages(library(rio))
suppressMessages(library(data.table))

opts <- docopt(doc)
# what are the options? Note that stripped versions of the parameters are added to the returned list
# str(opts)
ofile = opts$o
W = as.numeric(opts$W)
H = as.numeric(opts$H)
group = NA
if(is.null(opts$g) == F){
  group = opts$g
}
xname = 'Odds Ratio'
if(is.null(opts$x) == F){
  xname = opts$x
}
xlim = c()
if(is.null(opts$xlim) == F){
  xlim = as.numeric(unlist(strsplit(opts$xlim,',')))
}
myxratio=0.8
if(is.null(opts$xr) == F){
  myxratio = as.numeric(opts$xr)
}

# check.names = F, to make the header can contain special characters.
data = read.table(file("stdin"),header = T,sep="\t", check.names = FALSE)
colnames(data) = str_replace_all(colnames(data),'X_n_','\n')
colnames(data) = str_replace_all(colnames(data),'_n_','\n')

# Format P value.
if ('\nPVALUE' %in% colnames(data)){
    data[,'\nPVALUE'] = formatC(data[,'\nPVALUE'], digits = 2, format = "e")
}
if ('PVALUE' %in% colnames(data)){
    data[,'PVALUE'] = formatC(data[,'PVALUE'], digits = 2, format = "e")
}
#print(data)


#rnames = c('BETA','BETAL','BETAR') #columns for required.
rnames = c('OR','OR_CI_L','OR_CI_R') #columns for required.
# TEXTs to toshow
texts = data %>% select(-!!rnames) %>% as.data.table()
# make single line title to double line title to normalize the layout.
if(sum(str_detect(colnames(texts),'\n')) == 0){
    y = rep('\n', length(colnames(texts)))
    colnames(texts) = paste0(y, colnames(texts))
}

layout_with_group = F
if( is.na(group) == F){
  # Import to use data.table split. more advance, can keep order.
  texts = split(texts,by=group,keep.by = F)
  layout_with_group = T
}

# make it a little big longer than the default.
refline.y.extend = 1.1 # the top Y position for Y axis. single group as 1.1, multiple group as 1.1
my_section_sep=0
my_y_title_offset = 1.0  # the vertical space between title line and data.
# titleBase 2.0 for more than one group double line title, 2.1 for one group double line title.
# this can set the distance between title line with title text.
titleBase = 2.0 
if (layout_with_group){
   my_section_sep=0.6
   my_y_title_offset = 2.0
   refline.y.extend = 1.1
}
if (layout_with_group == F){
    texts$'group' = ''
    texts = split(texts,by='group',keep.by = F)
    my_section_sep=0
    my_y_title_offset = 1.6 # the vertical space between title line and data.
    titleBase = 2.1
}

#----------------------------------------------------------------------
##  https://github.com/tagteam/Publish
### Code: https://github.com/tagteam/Publish/blob/8a80218ff718812cdcc6000181504b8358e1effe/R/prepareLabels.R
prepareLabels <- function(labels,titles,...){
    labs <- labels
    tits <- titles
    labels <- labs$labels
    titles <- tits$labels
    labs$labels <- NULL
    tits$labels <- NULL
    if (is.matrix(labels)) {
        cnames <- colnames(labels)
        labels <- lapply(1:ncol(labels),function(j)labels[,j])
        names(labels) <- cnames
    }
    if (is.factor(labels) || is.numeric(labels) || is.character(labels)) 
        labels <- list(" "=labels)
    ncolumns <- length(labels)
    if (is.null(titles)){
        titles <- names(labels)
        do.titles <- TRUE
        if (is.null(titles)){
            do.titles <- FALSE
        }
    } else do.titles <- TRUE
    if (do.titles && length(titles)!=length(labels)){
        message(paste("Wrong number of titles: there are",ncolumns,"columns but ",length(titles),"title labels:",paste(titles,collapse=", ")))
    }
    if (length(labs$cex)<ncolumns){
        labs$cex <- rep(labs$cex,length.out=ncolumns)
    }
    if (length(tits$cex)<ncolumns){
        tits$cex <- rep(tits$cex,length.out=ncolumns)
    }
    if (is.null(titles)) titles <- rep(" ",ncolumns)
    if (is.null(labs$interspc))
        labels.interspc <- 1
    else
        labels.interspc <- labs$interspc
    colwidths <- sapply(1:ncolumns,function(f){
                            strwidth("m",units="inches")*labels.interspc +
                                max(strwidth(titles[[f]],cex=tits$cex[[f]],units="inches"),
                                    strwidth(labels[[f]],cex=labs$cex[[f]],units="inches"))
                        })
    if (do.titles==FALSE) titles <- NULL
    list(labels=labels,
         labels.args=labs,
         titles=titles,
         titles.args=tits,
         ncolumns=ncolumns,
         columnwidths=colwidths)
}

plotLabels <- function(labels,
                       labels.args,
                       titles,
                       titles.args,
                       width,
                       ylim,
                       ncolumns,
                       columnwidths,
                       ## xpos,
                       stripes,
                       ...){
    ## available space (width) is divided according to relative widths
    labelrelwidth <- columnwidths/sum(columnwidths)
    colwidths <- labelrelwidth*width
    if (labels.args$pos==4)
        ## aligned on right hand
        xpos <- c(0,cumsum(colwidths)[-ncolumns])
    else
        ## aligned on left hand
        xpos <- cumsum(colwidths)
    ## empty plot
    plot(0,0,type="n",axes=FALSE,xlim=c(0,width),ylim=ylim,xlab="",ylab="")
    if (!missing(stripes) && length(stripes)>0){
        stripes$xlim <- c(0,width)
        do.call("stripes",stripes)
    }
    
    ## arrows(x0=0,x1=width,y0=12,y1=12,lwd=8,col="orange")
    ## abline(v=xpos,col=1:5)
    nix <- lapply(1:ncolumns,function(l){
                      labels.args$x <- xpos[[l]]
                      labels.args$labels <- labels[[l]]
                      labels.args$cex <- labels.args$cex[[l]]
                      do.call("text",labels.args)
                  })
    ## to avoid that expression(bold(CI[95])) is
    ## changed to bold(CI[95]) we make titles a list
    if (length(titles)==1) titles <- list(titles)
    if (length(titles)>0){
        ## title.columns <- lapply(1:ncolumns,function(cc){sprintf(fmt=fmt.columns[[cc]],titles[[cc]])})
        nix <- lapply(1:ncolumns,function(l){
                          titles.args$x <- xpos[[l]]
                          titles.args$labels <- titles[[l]]
                          titles.args$cex <- titles.args$cex[[l]]
                          do.call("text",titles.args)
                      })
    }
}

# plotConfidence = function (x, y.at, lower, upper, pch = 16, cex = 1, lwd = 1, 
#           col = 4, xlim, xlab, labels, title.labels, values, title.values, 
#           section.pos, section.sep, section.title = NULL, section.title.x, 
#           section.title.offset, order, leftmargin = 0.025, rightmargin = 0.025, 
#           stripes, factor.reference.pos, factor.reference.label = "Reference", 
#           factor.reference.pch = 16, refline = 1, title.line = TRUE, 
#           xratio, y.offset = 0, y.title.offset, digits = 2, format, 
#           extremearrows.length = 0.05, extremearrows.angle = 30, add = FALSE, 
#           layout = TRUE, xaxis = TRUE, ...)
# wavefancy@gmail.com
plotConfidence = function (x, y.at, lower, upper, pch = 16, cex = 1, lwd = 1, 
          col = 4, xlim, xlab, labels, title.labels, values, title.values, 
          section.pos, section.sep, section.title = NULL, section.title.x, 
          section.title.offset, order, leftmargin = 0.025, rightmargin = 0.025, 
          stripes, factor.reference.pos, factor.reference.label = "Reference", 
          factor.reference.pch = 16, refline = 1, title.line = TRUE, 
          xratio, y.offset = 0, y.title.offset, digits = 2, format, 
          extremearrows.length = 0.05, extremearrows.angle = 30, add = FALSE, 
          titleBase = 2.0, refline.y.extend = 1.5,
          layout = TRUE, xaxis = TRUE, ...)  
{
  if (!is.list(x)) 
    x <- list(x = x)
  m <- x[[1]]
  names(x) <- tolower(names(x))
  if (missing(lower)) {
    lower <- x$lower
  }
  if (missing(upper)) 
    upper <- x$upper
  if (missing(xlim)) 
    xlim <- c(min(lower) - 0.1 * min(lower), max(upper) + 
                0.1 * min(upper))
  if (missing(xlab)) 
    xlab <- ""
  NR <- length(x[[1]])
  if (length(lower) != NR) 
    stop(paste0("lower has wrong dimension. There are ", 
                NR, " contrasts but ", length(upper), " upper limits"))
  if (length(upper) != NR) 
    stop(paste0("upper has wrong dimension. There are ", 
                NR, " contrasts but ", length(upper), " upper limits"))
  if (!missing(labels) && (is.logical(labels) && labels[[1]] == 
                           FALSE)) 
    do.labels <- FALSE
  else do.labels <- TRUE
  if (!do.labels || (!missing(title.labels) && (is.logical(title.labels) && 
                                                title.labels[[1]] == FALSE))) 
    do.title.labels <- FALSE
  else do.title.labels <- TRUE
  if (do.labels && missing(labels)) {
    labels <- x$labels
    if (is.null(labels)) 
      do.labels <- FALSE
  }
  if (missing(labels)) 
    labels <- NULL
  if (!is.data.frame(labels) && is.list(labels)) {
    section.rows <- sapply(labels, NROW)
    nsections <- length(labels)
    if (sum(section.rows) != NR) 
      stop(paste0("Label list has wrong dimension. There are ", 
                  NR, " confidence intervals but ", sum(section.rows), 
                  " labels"))
  }
  else {
    nsections <- 0
    section.rows <- NULL
  }
  if (missing(y.at)) {
    at <- 1:NR
  }
  else {
    if (length(y.at) != NR) 
      stop(paste0("Number of y positions must match number of confidence intervals which is ", 
                  NR))
    at <- y.at
  }
  if (nsections > 0) {
    if (!missing(section.title) && length(section.title) > 
        0) {
      names(labels) <- section.title
    }
    do.sections <- TRUE
    section.title <- rev(names(labels))
    if (!is.data.frame(labels[[1]]) && is.list(labels[[1]])) {
      sublevels <- names(labels)
      labels <- lapply(1:length(labels), function(l) {
        cbind(sublevels[[l]], data.table::data.table(labels[[l]]))
      })
    }
    labels <- data.table::rbindlist(lapply(labels, data.table::data.table), 
                                    use.names = TRUE)
    section.pos <- cumsum(rev(section.rows))
  }
  else {
    if (!missing(section.title) && length(section.title) > 
        0) {
      if (missing(section.pos)) 
        stop("Need y-positions for section.titles")
      do.sections <- TRUE
    }
    else {
      do.sections <- FALSE
    }
  }
  oneM <- 0.5
  if (do.sections) {
    if (missing(section.title.offset)) 
      section.title.offset <- 1.5 * oneM
    if (missing(section.sep)) 
      section.sep <- 2 * oneM
    section.shift <- rep(cumsum(c(0, section.sep + rep(section.sep, 
                                                       nsections - 1))), c(section.pos[1], diff(section.pos)))
    section.pos + section.shift[section.pos]
    if ((sub.diff <- (length(at) - length(section.shift))) > 
        0) 
      section.shift <- c(section.shift, rep(section.title.offset + 
                                              section.shift[length(section.shift)], sub.diff))
  }
  else {
    section.shift <- 0
  }
  at <- at + section.shift
  if (length(y.offset) != NR) 
    y.offset <- rep(y.offset, length.out = NR)
  at <- at + y.offset
  if (do.sections) {
    section.y <- at[section.pos]
    section.title.y <- section.y + section.title.offset
  }
  else {
    section.title.y <- 0
  }
  if (missing(y.title.offset)) {
    if (do.sections) {
      y.title.offset <- 1.5 * oneM + section.title.offset
    }
    else {
      y.title.offset <- 1.5 * oneM
    }
  }
  title.y <- max(at) + y.title.offset
  rat <- rev(at)
  ylim <- c(0, at[length(at)] + 1)
  dimensions <- list(NumberRows = NR, xlim = xlim, ylim = ylim, 
                     y.at = at)
  if (!missing(values) && (is.logical(values) && values[[1]] == 
                           FALSE)) 
    do.values <- FALSE
  else do.values <- TRUE
  if (do.values == TRUE) {
    if (!missing(title.values) && (is.logical(title.values) && 
                                   title.values[[1]] == FALSE)) 
      do.title.values <- FALSE
    else do.title.values <- TRUE
  }
  else {
    do.title.values <- FALSE
  }
  if (do.values) {
    if (missing(values)) {
      if (missing(format)) 
        if (all(!is.na(upper)) && any(upper < 0)) 
          format <- "(u;l)"
        else format <- "(u-l)"
        values.defaults <- paste(pubformat(x[[1]], digits = digits), 
                                 apply(cbind(lower, upper), 1, function(x) formatCI(lower = x[1], 
                                                                                    upper = x[2], format = format, digits = digits)))
        if (!missing(factor.reference.pos) && is.numeric(factor.reference.pos) && 
            all(factor.reference.pos < length(values.defaults))) 
          values.defaults[factor.reference.pos] <- factor.reference.label
        if (do.title.values && (missing(title.values)) || 
            (!is.expression(title.values) && !is.character(title.values))) 
          title.values <- expression(paste(bold(Estimate), 
                                           " (", bold(CI[95]), ")"))
    }
    else {
      values.defaults <- values
      if (missing(title.values)) 
        title.values <- NULL
    }
  }
  else {
    values.defaults <- NULL
    title.values <- NULL
  }
  if (add == TRUE) 
    do.values <- do.title.values <- do.labels <- do.title.labels <- FALSE
  dist <- (at[2] - at[1])/2
  if (missing(stripes) || is.null(stripes)) 
    do.stripes <- FALSE
  else do.stripes <- stripes
  stripes.DefaultArgs <- list(col = c(prodlim::dimColor("orange"), 
                                      "white"), horizontal = seq(min(at) - dist, max(at) + 
                                                                   dist, 1), xlim = xlim, border = NA)
  if (xaxis) 
    do.xaxis <- TRUE
  xaxis.DefaultArgs <- list(side = 1, las = 1, pos = 0, cex = cex)
  xlab.DefaultArgs <- list(text = xlab, side = 1, line = 1.5, 
                           xpd = NA, cex = cex)
  plot.DefaultArgs <- list(0, 0, type = "n", ylim = ylim, xlim = xlim, 
                           axes = FALSE, ylab = "", xlab = xlab)
  points.DefaultArgs <- list(x = m, y = rat, pch = 16, cex = cex, 
                             col = col, xpd = NA)
  arrows.DefaultArgs <- list(x0 = lower, y0 = rat, x1 = upper, 
                             y1 = rat, lwd = lwd, col = col, xpd = NA, length = 0, 
                             code = 3, angle = 90)
  refline.DefaultArgs <- list(x0 = refline, y0 = 0, x1 = refline, 
                              #y1 = max(at), lwd = lwd, col = "gray71", xpd = NA)
                              #wavefancy@gmail.com
                              y1 = max(at)*refline.y.extend, lwd = lwd, col = "gray71", xpd = NA)
  if (missing(title.labels)) 
    title.labels <- NULL
  labels.DefaultArgs <- list(x = 0, y = rat, cex = cex, labels = labels, 
                             xpd = NA, pos = 4)
  title.labels.DefaultArgs <- list(x = 0, y = at[length(at)] + 
                                     y.title.offset, cex = NULL, labels = title.labels, xpd = NA, 
                                   font = 2, pos = NULL)
  values.DefaultArgs <- list(x = 0, y = rat, labels = values.defaults, 
                             cex = cex, xpd = NA, pos = 4)
  title.y <- at[length(at)] + y.title.offset
  title.values.DefaultArgs <- list(x = 0, y = title.y, labels = title.values, 
                                   cex = NULL, xpd = NA, font = 2, pos = NULL)
  if (do.sections) 
    #title.line.y <- (title.y + max(section.title.y))/2
    # wavefancy@gmail.come. titleBase = 2.1 for one group title, 2.0 for two group title.
    title.line.y <- (title.y + max(section.title.y))/titleBase
  else title.line.y <- title.y - 0.25
  #title.line.DefaultArgs <- list(x0 = -Inf, y0 = title.line.y, 
  title.line.DefaultArgs <- list(x0 = -Inf, y0 = title.line.y, 
                                 x1 = Inf, y1 = title.line.y, lwd = lwd, col = "gray71", 
                                 xpd = TRUE)
  section.title.DefaultArgs <- list(x = 0, y = section.title.y, 
                                    labels = section.title, cex = NULL, xpd = NA, font = 4, 
                                    pos = 4)
  smartA <- prodlim::SmartControl(call = list(...), keys = c("plot", 
                                                             "points", "arrows", "refline", "title.line", "labels", 
                                                             "values", "title.labels", "section.title", "title.values", 
                                                             "xaxis", "stripes", "xlab"), ignore = c("formula", "data", 
                                                                                                     "add", "col", "lty", "lwd", "ylim", "xlim", "xlab", "ylab", 
                                                                                                     "axes", "factor.reference.pos", "factor.reference.label", 
                                                                                                     "extremearrows.angle", "extremearrows.length"), defaults = list(plot = plot.DefaultArgs, 
                                                                                                                                                                     points = points.DefaultArgs, refline = refline.DefaultArgs, 
                                                                                                                                                                     title.line = title.line.DefaultArgs, labels = labels.DefaultArgs, 
                                                                                                                                                                     title.labels = title.labels.DefaultArgs, section.title = section.title.DefaultArgs, 
                                                                                                                                                                     stripes = stripes.DefaultArgs, values = values.DefaultArgs, 
                                                                                                                                                                     title.values = title.values.DefaultArgs, arrows = arrows.DefaultArgs, 
                                                                                                                                                                     xaxis = xaxis.DefaultArgs, xlab = xlab.DefaultArgs), 
                                  forced = list(plot = list(axes = FALSE, xlab = ""), xaxis = list(side = 1)), 
                                  verbose = TRUE)
  if (is.null(smartA$title.labels$pos)) 
    smartA$title.labels$pos <- smartA$labels$pos
  if (is.null(smartA$title.values$pos)) 
    smartA$title.values$pos <- smartA$values$pos
  if (is.null(smartA$title.labels$cex)) 
    smartA$title.labels$cex <- smartA$labels$cex
  if (is.null(smartA$section.title$cex)) 
    smartA$section.title$cex <- smartA$labels$cex
  if (is.null(smartA$title.values$cex)) 
    smartA$title.values$cex <- smartA$values$cex
  if (!missing(factor.reference.pos) && is.numeric(factor.reference.pos) && 
      all(factor.reference.pos < length(values.defaults))) {
    if (length(smartA$points$pch) < NR) 
      smartA$points$pch <- rep(smartA$points$pch, length.out = NR)
    smartA$points$pch[factor.reference.pos] <- factor.reference.pch
  }
  if (add == FALSE) {
    oldmar <- par()$mar
    on.exit(par(mar = oldmar))
    on.exit(par(mfrow = c(1, 1)))
    par(mar = c(0, 0, 0, 0))
    dsize <- dev.size(units = "cm")
    leftmarginwidth <- leftmargin * dsize[1]
    rightmarginwidth <- rightmargin * dsize[1]
    plotwidth <- dsize[1] - leftmarginwidth - rightmarginwidth
    if (do.labels) {
      preplabels <- prepareLabels(labels = smartA$labels, 
                                  titles = smartA$title.labels)
    }
    if (do.values) {
      prepvalues <- prepareLabels(labels = smartA$values, 
                                  titles = smartA$title.values)
    }
    if (do.labels) {
      if (do.values) {
        do.stripes <- rep(do.stripes, length.out = 3)
        names(do.stripes) <- c("labels", "ci", "values")
        if (missing(xratio)) {
          lwidth <- sum(preplabels$columnwidth)
          vwidth <- sum(prepvalues$columnwidth)
          xratio <- c(lwidth/(lwidth + vwidth) * 0.7, 
                      vwidth/(lwidth + vwidth) * 0.7)
        }
        labelswidth <- plotwidth * xratio[1]
        valueswidth <- plotwidth * xratio[2]
        ciwidth <- plotwidth - labelswidth - valueswidth
        mat <- matrix(c(0, c(1, 3, 2)[order], 0), ncol = 5)
        if (!missing(order) && length(order) != 3) 
          order <- rep(order, length.out = 3)
        if (layout) 
          layout(mat, width = c(leftmarginwidth, c(labelswidth, 
                                                   ciwidth, valueswidth)[order], rightmarginwidth))
      }
      else {
        do.stripes <- rep(do.stripes, length.out = 2)
        names(do.stripes) <- c("labels", "ci")
        if (missing(xratio)) 
          xratio <- 0.618
        labelswidth <- plotwidth * xratio[1]
        ciwidth <- plotwidth - labelswidth
        valueswidth <- 0
        if (!missing(order) && length(order) != 2) 
          order <- rep(order, length.out = 2)
        mat <- matrix(c(0, c(1, 2)[order], 0), ncol = 4)
        if (layout) 
          layout(mat, width = c(leftmarginwidth, c(labelswidth, 
                                                   ciwidth)[order], rightmarginwidth))
      }
    }
    else {
      if (do.values) {
        do.stripes <- rep(do.stripes, length.out = 2)
        names(do.stripes) <- c("ci", "values")
        if (missing(xratio)) 
          xratio <- 0.618
        valueswidth <- plotwidth * (1 - xratio[1])
        ciwidth <- plotwidth - valueswidth
        labelswidth <- 0
        mat <- matrix(c(0, c(2, 1)[order], 0), ncol = 4)
        if (!missing(order) && length(order) != 2) 
          order <- rep(order, length.out = 2)
        if (layout) 
          layout(mat, width = c(leftmarginwidth, c(ciwidth, 
                                                   valueswidth)[order], rightmarginwidth))
      }
      else {
        xratio <- 1
        ciwidth <- plotwidth
        do.stripes <- do.stripes[1]
        names(do.stripes) <- "ci"
        labelswidth <- 0
        valueswidth <- 0
        mat <- matrix(c(0, 1, 0), ncol = 3)
        if (layout) 
          layout(mat, width = c(leftmarginwidth, ciwidth, 
                                rightmarginwidth))
      }
    }
    dimensions <- c(dimensions, list(xratio = xratio, labelswidth = labelswidth, 
                                     valueswidth = valueswidth, ciwidth = ciwidth, layout = mat))
  }
  if (add == FALSE) 
    par(mar = oldmar * c(1, 0, 1, 0))
  if (do.labels) {
    if (do.stripes[["labels"]]) 
      preplabels <- c(preplabels, list(width = labelswidth, 
                                       ylim = ylim, stripes = smartA$stripes))
    else preplabels <- c(preplabels, list(width = labelswidth, 
                                          ylim = ylim))
    do.call("plotLabels", preplabels)
    if ((missing(title.line) || !is.null(title.line)) && 
        ((add == FALSE) & is.infinite(smartA$title.line$x0))) {
      smartA$title.line$x0 <- par()$usr[1]
      smartA$title.line$x1 <- par()$usr[2]
      do.call("segments", smartA$title.line)
      smartA$title.line$x0 <- -Inf
    }
  }
  if (do.sections) {
    do.call("text", smartA$section.title)
  }
  if (do.values) {
    if (do.stripes[["values"]]) 
      prepvalues <- c(prepvalues, list(width = valueswidth, 
                                       ylim = ylim, stripes = smartA$stripes))
    else prepvalues <- c(prepvalues, list(width = valueswidth, 
                                          ylim = ylim))
    do.call("plotLabels", prepvalues)
    if ((missing(title.line) || !is.null(title.line)) && 
        ((add == FALSE) & is.infinite(smartA$title.line$x0))) {
      smartA$title.line$x0 <- par()$usr[1]
      smartA$title.line$x1 <- par()$usr[2]
      do.call("segments", smartA$title.line)
      smartA$title.line$x0 <- -Inf
    }
  }
  if (add == FALSE) {
    do.call("plot", smartA$plot)
    if (do.stripes[["ci"]]) 
      do.call("stripes", smartA$stripes)
    if (do.xaxis == TRUE) {
      oldcexaxis <- par()$cex.axis
      on.exit(par(cex.axis = oldcexaxis))
      par(cex.axis = smartA$xaxis$cex)
      if (is.null(smartA$xaxis$labels)) 
        do.call("axis", smartA$xaxis)
    }
    do.call("mtext", smartA$xlab)
  }
  if (add == FALSE) {
    if (missing(refline) || !is.null(refline)) 
      do.call("segments", smartA$refline)
  }
  if (add == FALSE) {
    if (missing(title.line) || !is.null(title.line)) {
      if (is.infinite(smartA$title.line$x0)) {
        smartA$title.line$x0 <- par()$usr[1]
        smartA$title.line$x1 <- par()$usr[2]
      }
      do.call("segments", smartA$title.line)
    }
  }
  do.call("points", smartA$points)
  if (any(smartA$arrows$x0 > xlim[2], na.rm = TRUE) || any(smartA$arrows$x1 < 
                                                           xlim[1], na.rm = TRUE)) 
    warning("One or several confidence intervals are completely outside xlim. You should adjust xlim.")
  tooHigh <- smartA$arrows$x1 > xlim[2]
  tooHigh[is.na(tooHigh)] <- FALSE
  tooLow <- smartA$arrows$x0 < xlim[1]
  tooLow[is.na(tooLow)] <- FALSE
  if (any(c(tooHigh, tooLow))) {
    if (length(smartA$arrows$angle) < NR) 
      smartA$arrows$angle <- rep(smartA$arrows$angle, length.out = NR)
    if (length(smartA$arrows$length) < NR) 
      smartA$arrows$length <- rep(smartA$arrows$length, 
                                  length.out = NR)
    if (length(smartA$arrows$code) < NR) 
      smartA$arrows$code <- rep(smartA$arrows$code, length.out = NR)
    if (length(smartA$arrows$col) < NR) 
      smartA$arrows$col <- rep(smartA$arrows$col, length.out = NR)
    smartA$arrows$x0 <- pmax(xlim[1], smartA$arrows$x0)
    smartA$arrows$x1 <- pmin(xlim[2], smartA$arrows$x1)
    smartA$arrows$code[tooLow & tooHigh] <- 3
    smartA$arrows$code[tooLow & !tooHigh] <- 1
    smartA$arrows$code[!tooLow & tooHigh] <- 2
    smartA$arrows$angle[tooLow | tooHigh] <- extremearrows.angle
    smartA$arrows$length[tooLow | tooHigh] <- extremearrows.length
    aargs <- smartA$arrows
    for (r in 1:NR) {
      aargs$x0 <- smartA$arrows$x0[r]
      aargs$x1 <- smartA$arrows$x1[r]
      aargs$y0 <- smartA$arrows$y0[r]
      aargs$y1 <- smartA$arrows$y1[r]
      aargs$code <- smartA$arrows$code[r]
      aargs$col <- smartA$arrows$col[r]
      aargs$length <- smartA$arrows$length[r]
      aargs$angle <- smartA$arrows$angle[r]
      suppressWarnings(do.call("arrows", aargs))
    }
  }
  else {
    suppressWarnings(do.call("arrows", smartA$arrows))
  }
  dimensions <- c(smartA, dimensions)
  invisible(dimensions)
}

########## My own function starts from here ###########
pdf(ofile,width=W, height=H, pointsize=16)
# https://bookdown.org/ndphillips/YaRrr/plot-margins.html
# https://www.r-graph-gallery.com/74-margin-and-oma-cheatsheet.html
# par(mar = c(bottom, left, top, right))
# the default
# print(par('mar')) # 5.1 4.1 4.1 2.1
par(mar = c(3.5, 0, 3, 2))
#print(par('oma'))
if(is.null(opts$xlim) == F){ # set the X lim.
  plotConfidence(
                  #x = data$BETA,lower = data$BETAL, upper = data$BETAR
                  x = data$OR,lower = data$OR_CI_L, upper = data$OR_CI_R
                  ,labels = texts
                  #,title.labels=tnames
                  ,xlab = xname
                  ,xaxis.cex=1.0    # font size for x axis.
                  ,xlab.cex=0.8     # font size for x label.
                  ,xlab.line=1.8    # The space between X label with X tick values.
                  ,plot.log="x"
                  ,values=FALSE     # Hidden to show the values for beta and CI for beta. to want to show OR text instead.
                  #,order=c(1,2,3)
                  #,xratio=c(0.8,0.1)
                  ,xratio=myxratio
                  ,refline = 1,refline.col='black',refline.lty=2
                  ,refline.y.extend=refline.y.extend
                  ,xlim=xlim
                  ,y.title.offset=my_y_title_offset # the vertical space between title line and data.
                  ,section.sep=my_section_sep
                  ,titleBase = titleBase
                  ,title.line.col='black'
                  ,title.labels.cex = 1 # Set the font size for title line.
                  ,arrows.col='black'
                  ,points.col='black'
                  ,points.cex=1.5
                  ,arrows.lwd = 1.5
  #                 ,title.labels.pos=3
  #                 ,title.labels.y=10.5
  #                 ,title.labels.offset=0.5
  )
}else{
  plotConfidence(
                  #x = exp(data$BETA),lower = exp(data$BETAL), upper = exp(data$BETAR)
                  x = data$OR,lower = data$OR_CI_L, upper = data$OR_CI_R
                  ,labels = texts
                  #,title.labels=tnames
                  ,xlab = xname
                  ,xaxis.cex=1.0    # font size for x axis.
                  ,xlab.cex=0.8     # font size for x label.
                  ,xlab.line=1.8    # The space between X label with X tick values.
                  ,plot.log="x"
                  ,values=FALSE     # Hidden to show the values for beta and CI for beta. to want to show OR text instead.
                  #,order=c(1,2,3)
                  #,xratio=c(0.8,0.01)
                  ,xratio=myxratio
                  ,refline = 1 ,refline.col='black',refline.lty=2
                  ,refline.y.extend=refline.y.extend
                  # ,xlim=NULL
                  ,y.title.offset=my_y_title_offset # the vertical space between title line with data.
                  ,section.sep=my_section_sep    # the space between groups(splits).
                  ,titleBase = titleBase
                  ,title.line.col='black'
                  ,title.line.lwd = 1
                  ,title.labels.cex = 1 # Set the font size for title line.
                  ,arrows.col='black'
                  ,points.col='black'
                  ,points.cex=1.5
                  ,arrows.lwd = 1.5
                  # ,leftmargin=0.015
  #                 ,title.labels.pos=3
  #                 ,title.labels.y=10.5
  #                 ,title.labels.offset=0.5
  )
}


#mtext('Top percentile',side=3, at=c(-4),line=1.5)
#text(-0.5,0,'TESTTESTTESTTEST')
t=dev.off()
