'
Generate formated MS Word document from the input CSV file.

Notes:
  * Read data from stdin and output results to files.

Usage:
  ForestPlot.R -o <filename> [-l] [-w ints] [--fn name] [--fs int]

Options:
  -o <filename> Output file name, audo add extension ".docx" . eg. example
  -l            Set the page layout as landscape
  -w ints       Set the column width. eg. 2|2,2,3
                  A single number set all column the same width.
                  A list of number set for each column, should match with input.
  --fs int      Set the font size, [11].
  --fn name     Set the font name, [Calibri].
  ' -> doc

# conda install -c conda-forge r-officer r-flextable

suppressMessages(library(flextable))
suppressMessages(library(officer))
suppressMessages(library(dplyr))
suppressMessages(library(docopt))


opts <- docopt(doc)
# what are the options? Note that stripped versions of the parameters are added to the returned list
# str(opts)
ofile  = paste(opts$o,'.docx',sep = '')
cwidth = if(is.null(opts$w)) c() else opts$w %>% strsplit(.,',') %>% unlist %>% as.numeric()
fn     = if(is.null(opts$fn)) 'Calibri' else opts$fn
fs     = if(is.null(opts$fs)) 11        else as.numeric(opts$fs)

# check.names = F, to make the header can contain special characters.
# read in csv file.
data = read.table(file("stdin"),header = T,sep=",", check.names = FALSE)
# data = import(stdin())

psize = 5
ft = flextable(data)
ft = ft %>% 
    #theme_zebra(., odd_header = "transparent", even_header = "transparent") %>%
    # hline(., border = fp_border(width = .5, color = "#007FA6"), part = "body" ) %>%hy
    # Set as three lines style, two for top header, and one for the bottom.
    hline(., border = fp_border(width = 1.0, color = "black"), part = "header" ) %>%
    hline_bottom(., j = NULL, border = fp_border(width = 1.5, color = "black"), part = "body") %>%
    hline_top(., j = NULL, border = fp_border(width = 1.5, color = "black"), part = "header") %>%
    #hline(., border = fp_border(width = 2, color = "#007FA6"), part = "header" ) %>%
    # line_spacing + valign not work properly in MS world, so we use padding instead.
    #line_spacing(., space=1.5, part="all") %>%
    #valign(.,valign = "bottom", part = "all") %>%
    align(., align = "center", part = "all") %>%
    # first column as left align
    align(., j=1,align = "left", part = "all") %>%
    padding(.,padding.top=psize, padding.bottom = psize, part = "all") %>%
    autofit

if(length(cwidth) >0 ){
    if(length(cwidth) == 1){
        ft = width(ft, width = cwidth[1])
    }else{
        if(dim(data)[2] != length(cwidth)){
            message('ERROR: The number of elements for -w should match the number of input column!')
            q()
        }else{
            for(i in 1:length(cwidth)){
                ft = width(ft, j = i, width = cwidth[i])
            }
        }
    }
}
# Set up the font size and font name.
ft = font(ft, fontname = fn, part = "all")
ft = fontsize(ft, size = fs, part = "all")

doc <- read_docx()
# How to set set up page layout.
# https://rdrr.io/cran/officer/man/prop_section.html
# https://davidgohel.github.io/officer/articles/offcran/word.html

doc <- doc %>% body_add_flextable(., value = ft)
#     #body_end_section_continuous()%>% 
#     body_add_flextable(., value = ft) %>% body_end_section_landscape() 
if(opts$l){
    doc <- doc %>% body_end_section_landscape() 
}
print(doc, target = ofile)