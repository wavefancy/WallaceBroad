wecho "
      python3 ./wcat.py test1.txt.gz test2.txt test3.txt.zst
    !!python3 ./wcat.py -c log.txt -a -m 'MYLOG' test1.txt.gz test2.txt test3.txt.zst
    !!ls test* | python3 ./wcat.py -i -c log.txt -a -m 'STDIN'
"

#A
#B
#1
#2
#3
#
#4
