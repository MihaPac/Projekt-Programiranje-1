import re
import orodja

stran = open('antike.html', 'r')

#spet koda s predavanj
regex_ebaya = re.compile(
    r"<h3 class=\"lvtitle\"><a/.*?\"class=\"vip\" title=\".*?\">(?P<ime>.*?)</a>.*?"#ime
    r'<li class="lvprice prc"><span  class="bold">.(?P<cena>\S*?)</span></li><li class="lvformat"><span >(?P<cena_ekstra>or Best Offer|Buy It Now|\d+? bids</span></li>.*?'#cena in best offer/buy it now/bids
    r'(?P<free_ship><label for="e1-76"><span class="cbx">Free international shipping</span></label>|).*?'#Free shipping
    r'<span aria-label="Ending time: " class="\D*? timeMs" timeMs="(?P<cas>\d{13})"></span>.*?'#Cas ko bo poteklo, unix time
    r'</ul><ul class="lvdetails left space-zero full-width"><li >From (?P<drzava>\D*?)</li><li >.*?'#izvor
    r'(?P<rated>http://ir.ebaystatic.com/pictures/aw/pics/s_1x2.gif)|).*?',#top rated seller
    flags=re.DOTALL
)

#if rated == '' then not trusted
#cene bojo samo v dolarjih
def pocisti_stvar(stvar):
    podatki = stvar.groupdict()
    podatki['ime'] = str(podatki['id'])
    podatki['cena'] = re.sub(',|\.','', podatki['cena'])
    podatki['cena_ekstra'] = (podatki['cena_ekstra'])
    if podatki['free_ship'] == '':
        podatki['free_ship'] = False
    else:
        podatki['free_ship'] = True
    podatki['cas'] = int(int(podatki['cas'])/1000)
    podatki['drzava'] = podatki['drzava']
    if podatki['rated'] == '':
        podatki['rated'] = False
    else:
        podatki['rated'] = True
    print(podatki)
    return podatki

def izloci_podatke_stvari(imenik):
    stvari = []
    for html_datoteka in orodja.datoteke(imenik):
        print(html_datoteka)
        for stvar in re.finditer(regex_ebaya, orodja.vsebina_datoteke(html_datoteka)):
            print(stvar)
            stvari.append(pocisti_stvar(stvar))
    print(stvari)
    return stvari

stvari = izloci_podatke_stvari('Html/')
orodja.zapisi_tabelo(stvari, ['ime', 'cena', 'cena_ekstra', 'free_ship', 'cas', 'drzava', 'rated'], 'test.csv')

'''
<span aria-label="Ending time: " class="SUNDAY timeMs" timeMs="1478477672000"></span> == 4d 12h left (Monday, 1AM)
<span aria-label="Ending time: " class="HOURS timeMs" timeMs="1478096082000"></span> ==  2h left (Today 3:14PM)
<span aria-label="Ending time: " class="TOMORROW timeMs" timeMs="1478217826000"></span> ==  1d 12h left (Friday, 1AM)

1478088013
1478477672000'''

#title > price (+ best offer or buy now or bids) > free shipping > time left > place > top rated 
