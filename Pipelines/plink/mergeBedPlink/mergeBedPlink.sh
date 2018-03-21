
#!/usr/bin/env bash

# Usage:
#   bash mergeBedPlink.sh ouput_file_base  input1_file_base intput2_file_base
#
#---------Merge two plink data------------------
# Version 3.0
# *******Important:
# *** Make it can be run in parallel.
# **********
#
# 1. remove AT/GC variants sites, can't resolve strand problem for these type of sites.
# 2. remove duplicated snps in file1.
# 3. only keep commom snps.
# 4. Remove sites even strand flip will be failed.
# 5. update snpID in file2 to match file1.
# 6. merge two files, do clean.

out=$1             #output file base with path
fbase1=$2           #file base with folder path.
fbase2=$3

#remove AT/GC sites, and sites with duplicate ids.
random=$RANDOM
#wecho -b '&&' "
wecho "
  # work out the overlapping position between two data set.
  # Remove duplicate sites.
  # Remove A/T, G/C sites.
  # Do merge and do clean.

  cat $fbase1.bim | CheckDuplicateByKey.py -k1,4 x y
  #Remove A/T, G/C sites.
  | ATCGVariants.py -a 5 -b 6 -r
  | wcut -f1,4
  | SubsetByKeyV3.py
     <(cat $fbase2.bim
        | CheckDuplicateByKey.py -k1,4 x y
        | ATCGVariants.py -a 5 -b 6 -r
        | wcut -f1,4)
     i 1,2
  >${random}_temp_overlap.txt

&&
#sites fail even after strand flip.
    StrandCheck.py
       <(cat $fbase1.bim | wcut -f1,4,5,6 | SubsetByKeyV3.py ${random}_temp_overlap.txt i 1,2 | sed 's|\t|:|')
       <(cat $fbase2.bim | wcut -f1,4,5,6 | SubsetByKeyV3.py ${random}_temp_overlap.txt i 1,2 | sed 's|\t|:|')
       1 2 3
     >${random}_temp_flip_OK.txt
    2>${random}_temp_flip_err.txt

&&
  plink --bfile $fbase1
     --extract
          <(cat $fbase1.bim | SubsetByKeyV3.py ${random}_temp_overlap.txt i 1,4 | wcut -f2)
     --exclude
          <(cat $fbase1.bim | SubsetByKeyV3.py <(cat ${random}_temp_flip_err.txt | wcut -f1 | sed 's|:|\t|') i 1,4 | wcut -f2)
     --allow-no-sex
     --make-bed --out ${random}_temp1
&&
  plink --bfile $fbase2
     --extract
          <(cat $fbase2.bim | SubsetByKeyV3.py ${random}_temp_overlap.txt i 1,4 | wcut -f2)
     --exclude
          <(cat $fbase2.bim | SubsetByKeyV3.py <(cat ${random}_temp_flip_err.txt | wcut -f1 | sed 's|:|\t|') i 1,4 | wcut -f2)
     --allow-no-sex
     --make-bed --out ${random}_temp2

&&
  #bug in plink1.9 for --bmerge reading bim from substitution, prepare the bim file.
  cat ${random}_temp2.bim
    | ColumnReplacer.py 2 *=NA
    | KeyMapReplacer.py -p <(cat ${random}_temp1.bim | wcut -f1,4,2) -k 1,4 -r 2
    >${random}_temp2_new.bim
&&
  #merge files.
  plink --bed ${random}_temp2.bed
        --fam ${random}_temp2.fam
        --bim ${random}_temp2_new.bim
        --bmerge ${random}_temp1
        --exclude <(echo 'NA')
        --allow-no-sex
        --make-bed
        --out $out
&&
  rm ${random}_*
"
