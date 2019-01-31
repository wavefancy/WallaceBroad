
cat test.stdin.txt | julia ClosestNumber.jl -f test.txt -c 2

cat test.stdin.txt | julia ClosestNumber.jl -f test.g.txt -c 2 -g 1 -t Float64
