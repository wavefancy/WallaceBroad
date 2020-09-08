
parallel -j 1 -q wecho "
  convert -compress lzw -density 600 -define profile:skip=ICC -trim -background white ./{}.pdf trim.{}.tiff
" ::: 1row_3columns
