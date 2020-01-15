'
Generate Forest Plot by the Publish package.

Notes:
  * Read data from stdin and output results to files.
  * The "OR,CIL,CIR" are required 3 colums, for OR and ORCI.
  * All the other colums are copied and to show on the plot.
  * INPUT format are tsv file.

Usage:
  ForestPlot.R -o <filename> -W float -H float [-g name] [-x xlabel] [--xlim nums]

Options:
  -o <filename> Output file name, in pdf format. eg. example.pdf
  -W float      The width of the output figure.
  -H float      The height of the output figure.
  -g name       Split the input by "name", plot each susbset by a section.
  -x xlabel     Set the X label name, default "Log(Odds Ratio)".
  --xlim nums   Set the xlim, num1,num2

  ' -> doc

# Generate Forest plot.
suppressMessages(library(Publish))
suppressMessages(library(tidyverse))
suppressMessages(library(docopt))
suppressMessages(library(rio))
suppressMessages(library(data.table))

opts <- docopt(doc)
# what are the options? Note that stripped versions of the parameters are added to the returned list
# str(opts)
# str(opts$g)
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

# check.names = F, to make the header can contain special characters.
data = read.table(file("stdin"),header = T,sep="\t", check.names = FALSE)
colnames(data) = str_replace_all(colnames(data),'X_n_','\n')
colnames(data) = str_replace_all(colnames(data),'_n_','\n')

#rnames = c('BETA','BETAL','BETAR') #columns for required.
rnames = c('OR','CIL','CIR') #columns for required.
# TEXTs to toshow
texts = data %>% select(-!!rnames) %>% as.data.table()
if( is.na(group) == F){
  # Import to use data.table split. more advance, can keep order.
  texts = split(texts,by=group,keep.by = F)
}
#pdf(paste0(oname, '.pdf'),width=9,height=4.5,pointsize=16)
pdf(ofile,width=W, height=H, pointsize=16)

if(is.null(opts$xlim) == F){ # set the X lim.
  plotConfidence(
                  #x = data$BETA,lower = data$BETAL, upper = data$BETAR
                  x = data$OR,lower = data$CIL, upper = data$CIR
                  ,labels = texts
                  #,title.labels=tnames
                  ,xlab = xname
                  ,xaxis.cex=1.0    # font size for x axis.
                  ,xlab.cex=0.8     # font size for x label.
                  ,xlab.line=1.8    # The space between X label with X tick values.
                  ,plot.log="x"
                  ,values=FALSE     # Hidden to show the values for beta and CI for beta. to want to show OR text instead.
                  ,order=c(1,2,3)
                  ,xratio=c(0.8,0.1)

                  ,refline = 1,refline.col='black',refline.lty=2
                  ,xlim=xlim
                  ,y.title.offset=2.3 # the vertical space between title line with value.
                  ,section.sep=0.6    # the space between groups(splits).
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
                  x = data$OR,lower = data$CIL, upper = data$CIR
                  ,labels = texts
                  #,title.labels=tnames
                  ,xlab = xname
                  ,xaxis.cex=1.0    # font size for x axis.
                  ,xlab.cex=0.8     # font size for x label.
                  ,xlab.line=1.8    # The space between X label with X tick values.
                  ,plot.log="x"
                  ,values=FALSE     # Hidden to show the values for beta and CI for beta. to want to show OR text instead.
                  ,order=c(1,2,3)
                  ,xratio=c(0.8,0.1)

                  ,refline = 1,refline.col='black',refline.lty=2
                  # ,xlim=NULL
                  ,y.title.offset=2.3 # the vertical space between title line with value.
                  ,section.sep=0.6    # the space between groups(splits).
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
}


#mtext('Top percentile',side=3, at=c(-4),line=1.5)
#text(-0.5,0,'TESTTESTTESTTEST')
t=dev.off()
