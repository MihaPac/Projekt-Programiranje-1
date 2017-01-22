import os

novo = set()
f = open("izdelki_ebay_bid.csv", "r")
for line in f:
    print((line,))
    novo.union((line,))
g = open("bids.csv", "w")
print(novo)
g.close()
f.close()
