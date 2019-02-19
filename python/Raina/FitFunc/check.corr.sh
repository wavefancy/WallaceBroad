# Check the correlation of fitted values with true values. 

echo '>corr.txt'
parallel -j 1 -q wecho "
paste
	<(cat ctrl_ctrl.txt | tail -n +2 | wcut -f{})
	<(cat fitted.values.txt | wcut -f{})
| datamash ppearson 1:2	>> corr.txt
" :::: <(seq 1 1 15)
