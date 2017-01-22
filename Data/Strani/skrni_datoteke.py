import re
import orodja
import os

regex = re.compile(r'(?P<Vse><ul id="ListViewInner">.*?<div id="PaginationAndExpansion)', flags=re.DOTALL)

f = open('../Kategorije/kategorije.csv', 'r')
kategorije = []
datuma = ['20.01.2016', '21.01.2016']

for line in f:
    csv_stvari = line.split(',')
    kategorije += [csv_stvari[1]]
kategorije = kategorije[1:]

def pocisti_html(html):
    podatki = html.groupdict()
    podatki['Vse'] = podatki['Vse']
    return podatki['Vse']


def funkcija_ki_zbira_podatke(regex):
   izdelki = ''
   for kategorija in kategorije:
       for dan in datuma:  
            for i in range(1,21):
                if os.path.isfile('{}-stran{}-{}.html'.format(kategorija, i, dan)) == True:
                    #Yard-Garden-Outdoor-Living-stran20-26.10.2016.html
                    #print('{}-stran{}-{}.html'.format(kategorija, i, dan))
                    for izdelek in re.finditer(regex, orodja.vsebina_datoteke('{}-stran{}-{}.html'.format(kategorija, i, dan))):
                        izdelki += pocisti_html(izdelek)
                        #print(len(izdelki))
                    g = open('Novi-{}-{}-{}.html'.format(kategorija, i, dan), 'w')
                    g.write(izdelki)
                    g.close()
                    izdelki = ''
   return None

funkcija_ki_zbira_podatke(regex)
