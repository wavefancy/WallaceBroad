#convert the data in json format.
#cat test.txt | python3 LocusZoomJson.py

python3 JSON2HTML.py -r 1:150010660-151010660 -j json.CAD-1-150510660.json,json.MIG-1-150510660.json -t 'CAD,MIG' >test_good.html
#python3 JSON2HTML.py -r 10:114550452-115067678 -j assoc_10_114550452-115067678.json,assoc_10_114550452-115067678.json -t 'CAD,MIG' >test.html
