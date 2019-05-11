# Generate forest plot for odds ratio.
# http://www.metafor-project.org/doku.php/plots:forest_plot_with_subgroups

library(metafor)
#library(forestplot)

# *************
# A simi-auto plot for forest plot.
# @Wallace Wang, wavefancy@gmail.com
# *************


#http://www.cookbook-r.com/Graphs/Output_to_a_file/
pdf("plots.pdf", width=6, height=3.2)
### decrease margins so the full space is used
par(mar=c(4,4,1,2))

data=read.table("data.txt",header = T,sep = '\t')

# Specify study group.
# slab	optional vector with labels for the k studies.
# data is data.frame with header.  author year tpos  tneg cpos  cneg ablat      alloc
### fit random-effects model (use slab argument to define study labels)
#res <- rma(ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg, measure="RR",
#           slab=paste(author, year, sep=", "), method="REML")

# we estimate the OR and its 95%CI based on 2x2 table.
#res <- rma(ai=t.case, bi=t.ctrl, ci=r.case, di=r.ctrl, data=data, measure="OR",
#           slab=paste(percentile, '%', sep=""),
#           method="REML")
#res$slab = paste(data$percentile, '%', sep="")


### set up forest plot (with 2x2 table counts added; rows argument is used
### to specify exactly in which rows the outcomes will be plotted)
# forest(res, xlim=c(-16, 6), at=log(c(0.05, 0.25, 1, 4)), atransf=exp,
#        ilab=cbind(dat.bcg$tpos, dat.bcg$tneg, dat.bcg$cpos, dat.bcg$cneg),
#        ilab.xpos=c(-9.5,-8,-6,-4.5), cex=0.75, ylim=c(-1, 27),
#        order=order(dat.bcg$alloc), rows=c(3:4,9:15,20:23),
#        xlab="Risk Ratio", mlab="", psize=1)

# https://www.rdocumentation.org/packages/metafor/versions/1.9-9/topics/forest.rma
# https://stackoverflow.com/questions/32655316/using-meta-metaprop-and-forest-to-create-forest-plot-graphics-in-r

# Data for each group on the Y. Num_data_entry + 3 (title + 2 empty line). Plot in reverse order
# we have 4 group, each has 4 data entries. + 2 empty lines for the sperator between groups.
# So we will put data at 1:4,7:10,13:16,19:22
# put title for each group at 5, 11, 17, 23
# Ylim top is the total lines: 22 + 4(extra lines) = 26.

# YLIM = #data_entries + (#group -1) * 2 + 4(extra_lines)
YLIM = dim(data)[1] + (length(unique(data$GROUP)) -1) *2 + 4

# Compute the location for put each row's text.
num_per_group = length(data$GROUP)/length(unique(data$GROUP))
num_of_group  = length(unique(data$GROUP))
shift_num = num_per_group + 2
x = 1:num_per_group
yrows = x
k = num_per_group +1
ylables = c(k)
for (y in 1:(num_of_group-1)) {
  x = x + shift_num
  k = k + shift_num
  yrows = c(yrows, x)
  ylables = c(ylables, k)
}
# the y position for put each row's data entry.
yrows
# the y position for put each labels.
ylables

#col_pos_4data_cols = c(-7.5,-6,-3,-1.5)
# by is the length between columns, the last number is teh sift from 0
# ****** Control the column width behaviours here ******
col_width = 2.8
shift_left = 1.5
label_width = 4.8
XRIGHT = 6
# ************************

col_pos_4data_cols = rev( seq(0,by=col_width * - 1.0,length.out = 4) - shift_left )
XLEFT = col_pos_4data_cols[1] - label_width
# we use the Forest Plots (Default Method) for specify the size and variance(CI) by our self.
#forest(res,
forest(x=data[,6],ci.lb = data[,7], ci.ub = data[,8], slab= data[,1],
       xlim=c(XLEFT, XRIGHT),
       #at=log(c(0.5, 1, 3, 8)),
       at = c(0,1,2),
       #atransf=exp,
       #atransf=log,
       #The 4 columns for listing scores.
       #ilab=cbind(data$t.case, data$t.ctrl, data$r.case, data$r.ctrl),
       ilab = data[,2:5],
       # important change ylim from ylim=c(-1, 20) to ylim=c(0.5, 20) to hidden the summary information.
       #ilab.xpos=c(-7.5,-6,-3,-1.5), cex=0.75,
       ilab.xpos=col_pos_4data_cols, cex=0.75,
       #ylim=c(0.5, 26),
       ylim=c(0.5, YLIM),
       #rows, specify the position on Y for result to put.
       #rows=c(1:4,7:10,13:16,19:22),
       rows=rev(yrows),
       #col=fpColors(box="royalblue",line="darkblue", summary="royalblue"),
       xlab="Odds Ratio", psize=1)

op <- par(cex=0.75, font=3)
### add text for the subgroups, text, x y location.
#text(-13, c(23,17,11,5), pos=4, c("UK Biobank White","UK Biobank S.Asian",
#                               "Medgenome S.Asian",
#                               "BRAVE"))
# We put label data in reverse order.
text(XLEFT, rev(ylables), pos=4, unique(data$GROUP))

### switch to bold font
par(font=2)
### add column headings to the plot, top limit is 26.
#text(c(-7.5,-6,-3,-1.5), 25, c("Case", "Control", "Case", "Control"))
text(col_pos_4data_cols , YLIM-1, colnames(data)[2:5])
#GROUP NAMEs for the columns of 2:3, 4:5
#text(c(-6.65,-2.15),      YLIM, c("Top percentile", "Remainder population"))
text(XLEFT,               YLIM-1, colnames(data)[1],  pos=4)
text(XRIGHT,              YLIM-1, "Odds Ratio [95% CI]", pos=2)

dev.off()
