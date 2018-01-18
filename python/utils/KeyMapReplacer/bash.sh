
cat in.txt | python3 KeyMapReplacer.py -p kv_map.txt -k 1,2 -a N

#1       a       3       N
#2       c       4       10
#3       d       5       N

cat in.txt | python3 KeyMapReplacer.py -p kv_map.txt -k 1,2 -r 3

#1       a       3
#2       c       10
#3       d       5

cat in.txt | python3 KeyMapReplacer.py -p kv_map1.txt -k 1 -r 3
#Warning: Duplicate keys, only keep first entry. Skip: 2   c
#Warning: Duplicate keys, only keep first entry. Skip: 2   a
#1       a       3
#2       c       K
#3       d       5
