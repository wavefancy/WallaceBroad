# update version of CheckInRangeCHR.py
cat in.txt | python3 CheckInRangeCHR.py -r range.txt -c 1 -p 2

cat in.txt | python3 CheckInRange.py -r <(cat range.txt | wcut -f2,3) -c 2 -e
