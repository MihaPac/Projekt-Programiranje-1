# -*- coding: utf-8 -*-

import re
import orodja
import csv
import time

#time.strftime('%d.%m. %Hh%Mmin%Ss')

#to bo iskalo html datoteke o samih izdelkih znotraj kategorij
#nesmem pozabiti tu poiskati število "listings"

#dobiti html_ime iz kategorije.csv

#Vsaj dvesto kategorij je, če iz vsake vzamem 20 strani bom imel 4000 izdelkov iz vsake in vse
#skupaj bom imel približno 8 000 000 izdelkov.
f = open('../Kategorije/kategorije.csv', 'r')
kategorije = {}

for line in f:
    if line == '\n':
        continue
    else:
        csv_stvari = line.split(',')
        kategorije[csv_stvari[0]] = [csv_stvari[1]]

#spet vzeta koda iz predavanj
#https://github.com/matijapretnar/programiranje-1/blob/master/ap-1-zajem-podatkov/predavanja/shrani_strani.py

#ta naslednja koda je grozota ampak deluje tako, da kategorija pomeni številka iz csv datoteke
#človeku prijaznejši prikaz za ime datotek pa dobim iz kategorije[kategorija]
stevilo = 0 #to zgolj da vidim kako dolgo do konca je se

for kategorija in kategorije:
    stevilo += 1 * 20
    print(stevilo/100)
    for stran in range(1, 21):
        html_osnova = 'http://www.ebay.com/sch/' + str(kategorija) + '/i.html?_pgn=' + str(stran)+ '&_skc=200&_sop=1&_ipg=200'
        #datoteka = '/Data/Html_Strani/' + 'ebay' + kategorije[kategorija][0] + '-stran{}'.format(stran) + time.strftime('%d.%m.2016') + '.html'
        datoteka = '{}-stran{:01}-{}.html'.format(kategorije[kategorija][0], stran, time.strftime('%d.%m.2016'))
        orodja.shrani(html_osnova, datoteka)
        

#to ne deluje ampak očitno ima ebay en API ki mi to lažje omogoča, ta datoteka se bo ohranila, če se API izkaže kot
#zanič
#API ne dovoljuje uporabe za zbiranje statističnih podatkov
#Možno, da ebay ne dovoljuje takih programov, javi samo ！ ko zaženem program
#Problem enkodiranja se poja včasih, včasih pa ne, nimam pojma kaj je s tem.
