'
Generate formated MS Word document from the input CSV file.

Notes:
  * Read data from stdin and output results to files.

Usage:
  ForestPlot.R -o <filename> 

Options:
  -o <filename> Output file name, audo add extension ".docx" . eg. example
  ' -> doc

# conda install -c conda-forge r-officer r-flextable

suppressMessages(library(flextable))
suppressMessages(library(officer))
suppressMessages(library(dplyr))
suppressMessages(library(docopt))


opts <- docopt(doc)
# what are the options? Note that stripped versions of the parameters are added to the returned list
# str(opts)
ofile = paste(opts$o,'.docx',sep = '')

# check.names = F, to make the header can contain special characters.
# read in csv file.
data = read.table(file("stdin"),header = T,sep=",", check.names = FALSE)
# data = import(stdin())

psize = 5
ft = flextable(data)
ft = ft %>% theme_zebra(., odd_header = "transparent", even_header = "transparent") %>%
    # hline(., border = fp_border(width = .5, color = "#007FA6"), part = "body" ) %>%
    hline(., border = fp_border(width = 2, color = "#007FA6"), part = "header" ) %>%
    # line_spacing + valign not work properly in MS world, so we use padding instead.
    #line_spacing(., space=1.5, part="all") %>%
    #valign(.,valign = "bottom", part = "all") %>%
    align(., align = "center", part = "all") %>%
    # first column as left align
    align(., j=1,align = "left", part = "all") %>%
    padding(.,padding.top=psize, padding.bottom = psize, part = "all") %>%
    autofit

doc <- read_docx()
doc <- body_add_flextable(doc, value = ft)
print(doc, target = ofile)