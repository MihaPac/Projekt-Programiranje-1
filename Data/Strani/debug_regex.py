import os
import re
import orodja
from functools import lru_cache
#regex za vse stvari
#Kaj iskati:  IME*, STEVILO PONUDB*, FREE SHIPPING, PREOSTALI CAS (UNIX?)/BUY NOW???,
#             LOKACIJA, ZAUPAN PRODAJALEC, CENA, 

#UPORABI TO, Z DOT-ALL
#\"\>(?P<Ime>\w.*?)<\/a>.*?\$(?P<Cena>.*?)<\/span>.*?(((?P<Bidders>\d+?) bids)|(?P<Now>Buy It Now)).*?(?P<Shipping>Free international shipping)?.*?timeMs=\"(?P<Cas>\d*).*?From (?P<Drzava>.+?\b).*?
#Potem ko si dobil podatke preveri kateri izdelki so od Top-rated sellers
#Edini problem z regexom je da za <Sold> vedno izbere '' namesto sold, tudi ce je podatek v string
regex_html = re.compile(r'Click this link to access .?*\"\>(?P<Ime>\w.*?)<\/a>.*?\$'
                        r'((?P<Cena>.*?)<\/span>.*?(((?P<Bidders>\d+?) bids)|(?P<Now>Buy It Now)).*?)'
                        r'(((?P<Sold>) sold)|).*?timeMs=\"'
                        #(?P<Shipping>Free international shipping)?
                        r'(?P<Cas>\d*).*?From (?P<Drzava>.+?\b)', flags=re.DOTALL)
f = open('../Kategorije/kategorije.csv', 'r')
kategorije = []
datuma = ['20.01.2016', '21.01.2016']

for line in f:
    csv_stvari = line.split(',')
    kategorije += [csv_stvari[1]]
kategorije = kategorije[1:]
#Koda spet vzeta iz predavanj https://github.com/matijapretnar/programiranje-1/blob/master/ap-2-urejanje-podatkov/predavanja/ustvari_csv.py
def pocisti_html(html):
    podatki = html.groupdict()
    podatki['Ime'] = (podatki['Ime'])
    podatki['Cena'] = (podatki['Cena'])
    if podatki['Sold'] == None:
        podatki['Sold'] = 'None'
    #podatki['Sold'] = podatki['Sold']
    if podatki['Bidders'] == None:
        podatki['Bidders'] = 'None'
    podatki['Bidders'] = (podatki['Bidders'])
    podatki['Now'] = podatki['Now']
    if podatki['Now'] == None:
        podatki['Now'] = 'None'
    #podatki['Shipping'] = (podatki['Shipping'])
    podatki['Cas'] = (podatki['Cas'])
    podatki['Drzava'] = podatki['Drzava']
##    print(podatki)
    print(podatki)
    return podatki


#kategorije delujejo
#print(datuma) deluje
#zdaj pa odpreti datoteke
def funkcija_ki_zbira_podatke():
   izdelki = []
   i = 18
   for kategorija in kategorije:
       for dan in datuma:
                if os.path.isfile('{}-stran{}-{}.html'.format(kategorija, i, dan)) == True:
                    #Yard-Garden-Outdoor-Living-stran20-26.10.2016.html
                    #print('{}-stran{}-{}.html'.format(kategorija, i, dan))
                    #deluje!!!!!!!!
                    for izdelek in re.finditer(regex_html, orodja.vsebina_datoteke('{}-stran{}-{}.html'.format(kategorija, i, dan))):
                        izdelki.append(pocisti_html(izdelek))
                        #print(len(izdelki))
                    funkcija_da_druga_dela(izdelki)
                    print(kategorija + str(i))
                    izdelki = []
   return None

def funkcija_da_druga_dela(izdelki):
    #print('0')
    podatki = izdelki
    #print('A')
    g = open('ebay_izdelki.csv', 'a')
    #print('B')
    for i in range(len(izdelki)):
        g.write(izdelki[i]['Ime'] + ',')
        g.write((izdelki[i])['Cena'] + ',')
        g.write((izdelki[i])['Bidders'] + ',')
        g.write((izdelki[i])['Sold'] + ',')
        g.write((izdelki[i])['Now'] + ',')
        g.write((izdelki[i])['Cas'] + ',')
        g.write((izdelki[i])['Drzava'] + '\n')
    #print('Pride do sem.')
    g.close()

funkcija_ki_zbira_podatke()
