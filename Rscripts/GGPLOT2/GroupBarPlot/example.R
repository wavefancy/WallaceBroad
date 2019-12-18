# Make group bar plot
# Based on the example
# http://www.sthda.com/english/articles/32-r-graphics-essentials/132-plot-grouped-data-box-plot-bar-plot-and-more/

library(dplyr) 
library(ggplot2)
library(ggpubr)
library(rio)
theme_set(theme_pubclean())

attach(diamonds)

df <- diamonds %>%
  filter(color %in% c("J", "D")) %>%
  group_by(cut, color) %>%
  summarise(counts = n(),sd=sd(price),mean=mean(price),se=sd(price)/sqrt(n())) 
head(df, 4)

ofile="test.pdf"
pdf(ofile,width=5.5, height=5.5)

p <- ggplot(df, aes(x = cut, y = mean)) +
  geom_bar(
    aes(color = color, fill = color),
    stat = "identity", position = position_dodge(0.8),
    width = 0.7
  ) +
  scale_color_manual(values = c("#0073C2FF", "#EFC000FF"))+
  scale_fill_manual(values = c("#0073C2FF", "#EFC000FF"))
p = p + geom_errorbar(aes(color = color, ymin = mean-se, ymax = mean+se), position = position_dodge(0.8), width = 0.2)
#p = p + geom_errorbar(aes(color = rep('black',10), ymin = mean-se, ymax = mean+se), position = position_dodge(0.8), width = 0.2)
p

graphics.off()