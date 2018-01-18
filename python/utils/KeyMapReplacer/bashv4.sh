
cat inv4.txt | python3 KeyMapReplacer.py -p kv_map4.txt -k 1 -a NA -d ';'

#Warning: Duplicate keys, only keep first entry. Skip: 2   c
#Warning: Duplicate keys, only keep first entry. Skip: 2   a
#1       a       3       NA
#2;4     c       4       K;NA
#3;2     d       5       NA;K

cat inv4.txt | python3 KeyMapReplacer.py -p kv_map4.txt -k 1 -r 2 -d ';'

#Warning: Duplicate keys, only keep first entry. Skip: 2   c
#Warning: Duplicate keys, only keep first entry. Skip: 2   a
#1       NA      3
#2;4     K;NA    4
#3;2     NA;K    5
