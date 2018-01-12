
cat test.txt | python3 ./qsubHelper.py -t 10 -m 5 -c 3 -n test

#qsub -cwd -l h_rt=10:0:0 -l h_vmem=5g -pe smp 3 -binding linear:3 -N test_1 -b y 'line1'
#qsub -cwd -l h_rt=10:0:0 -l h_vmem=5g -pe smp 3 -binding linear:3 -N test_2 -b y 'line2'
