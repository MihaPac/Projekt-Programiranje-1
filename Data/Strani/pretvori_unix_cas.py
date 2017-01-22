import os, time

import datetime
print(
    datetime.datetime.fromtimestamp(
        int("1484947989")
    ).strftime('%Y-%m-%d %H:%M:%S')
)

f = open('ebay_izdelki_zmanjsano_bid.csv', 'r')
for line in f:
    vrstica = line.split(',')
    if vrstica[5] == 'Cas':
        continue
    #print(vrstica[5])
    vrstica[5] = (datetime.datetime.fromtimestamp(
        int(vrstica[5][:10])
    ).strftime('%Y-%m-%d %H:%M:%S')
)
    print(vrstica[5])
    g = open('izdelki_ebay_bid.csv', 'a')
    g.write(
        vrstica[0] + ',' +
        vrstica[1] + ',' +
        vrstica[2] + ',' +
        vrstica[3] + ',' +
        vrstica[4] + ',' +
        vrstica[5] + ',' +
        vrstica[6] + ',' +
        vrstica[7]
        )
    g.close()
