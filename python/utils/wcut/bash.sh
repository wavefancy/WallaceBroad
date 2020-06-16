cat test3.txt | ./wcut.py -f1- -d ',' -a NA

# Add the function for seting output delimiter.
echo '1:151258778:T:C,1:151259079:A:AAGGTTCAAGCAATTCTTCTGCCTCAGCCTCCC,1:151260563:T:C' | python3 ./wcut.py -f1- -d ',' --od '+'
#1:151258778:T:C+1:151259079:A:AAGGTTCAAGCAATTCTTCTGCCTCAGCCTCCC+1:151260563:T:C
