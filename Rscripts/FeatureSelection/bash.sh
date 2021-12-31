
wecho "
	cat ../LogisticRegression/./test.txt 
	| /Users/minxianwang/miniconda3/envs/R/bin/Rscript ./FSExhaustiveSearch.R 
		-f 'c~lot1+lot2+G'
		#-f 'c~.'
		--family binomial -n 3
	> ./results.txt
"

