import re
import csv
import orodja

#to išče kategorije, in jih da v csv datoteko, imel bi še idejo, da bi dodal število izdelkov na prodajo, a ker se to
#število stalno spreminja bom moral to narediti takrat ko iscem produkte, in še takrat ne natančno

#kategorije = open("kategorije.html", 'r')

#vzeto iz predavanj

#v interesih transparence bom povedal, da je bila html datoteka samo ena in priredil sem jo, da bi regex deloval

regex_kategorije = re.compile(
    r'<li><a href="http://www.ebay.com/sch/(?P<html_ime>\D+?.*?)/(?P<id>\d+)/i.html" class="ch">(?P<ime>.*?)</a></li>',
    flags=re.DOTALL
)


def pocisti_kategorije(kategorija):
    podatki = kategorija.groupdict()
    podatki['id'] = int(podatki['id'])
    podatki['html_ime'] = (podatki['html_ime'])
    podatki['ime'] = (podatki['ime'])
    return podatki


def izloci_podatke_kategorij(imenik):
    kategorije = []
    for html_datoteka in orodja.datoteke(imenik):
        for kategorija in re.finditer(regex_kategorije, orodja.vsebina_datoteke(html_datoteka)):
            kategorije.append(pocisti_kategorije(kategorija))
    return kategorije


kategorije = izloci_podatke_kategorij('Data/Kategorije/')
orodja.zapisi_tabelo(kategorije, ['id', 'html_ime', 'ime'], 'Data/Kategorije/kategorije.csv')
