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
#Trije tipi: bid, buy now, oboje

regex_html_bid = re.compile(r'Click this link to access [ a-zA-z\#\&]{1,200}">(?P<Ime>[ a-zA-z0-9\.]*?)<\/a>.*?'
                              r'\$(?P<Cena_Bid>(\d|\.)*?)<\/span>.*?((?P<Bids>\d+?) bids).*'
                              r'?(?P<Cena_Buy>).*?(?P<Buy>).*?t'
                              r'imeMs="(?P<Cas>\d{13}).*?From (?P<Drzava>(\w|\s)*?)<\/li>', flags=re.DOTALL)
regex_html_buy = re.compile(r'Click this link to access [ a-zA-z\#\&]{1,200}">(?P<Ime>[ a-zA-z0-9\.]*?)<\/a>.*?'
                              r'\$(?P<Cena_Bid>).{1,200}(?P<Bids>).*'
                              r'?\$(?P<Cena_Buy>(\d|\.)*?)<\/span>.*?(?P<Buy>Buy It Now).*?t'
                              r'imeMs="(?P<Cas>\d{13}).*?From (?P<Drzava>(\w|\s)*?)<\/li>', flags=re.DOTALL)
regex_html_oboje = re.compile(r'Click this link to access .{1,200}">(?P<Ime>\w.*?)<\/a>.*?'
                              r'\$(?P<Cena_Bid>(\d|\.)*?)<\/span>.*?((?P<Bids>\d+?) bids).*'
                              r'?$(?P<Cena_Buy>(\d|\.)*?)<\/span>.*?(?P<Buy>Buy It Now).*?t'
                              r'imeMs="(?P<Cas>\d{13}).*?From (?P<Drzava>(\w|\s)*?)<\/li>', flags=re.DOTALL)
regex_html = re.compile(r'Click this link to access .*?\"\>(?P<Ime>\w.*?)<\/a>.*?\$'
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
def pocisti_html(html,kategorija):
    podatki = html.groupdict()
    podatki['Ime'] = (podatki['Ime'])
    if podatki['Cena_Bid'] == '':
        podatki['Cena_Bid'] = 'None'
    elif podatki['Cena_Bid'] != '':
        podatki['Cena_Bid'] = (podatki['Cena_Bid'])
    #if podatki['Sold'] == None:
    #    podatki['Sold'] = 'None'
    #podatki['Sold'] = podatki['Sold']
    if podatki['Bids'] == '':
        podatki['Bids'] = 'None'
    podatki['Bids'] = (podatki['Bids'])
    if podatki['Cena_Buy'] == '':
        podatki['Cena_Buy'] = 'None'
    elif podatki['Cena_Buy'] != '':    
        podatki['Cena_Buy'] = (podatki['Cena_Buy'])
    podatki['Buy'] = podatki['Buy']
    if podatki['Buy'] == '':
        podatki['Buy'] = 'None'
    #podatki['Shipping'] = (podatki['Shipping'])
    podatki['Cas'] = (podatki['Cas'])
    podatki['Drzava'] = podatki['Drzava']
    podatki['Kategorija'] = kategorija
##    print(podatki)
    return podatki


#kategorije delujejo
#print(datuma) deluje
#zdaj pa odpreti datoteke

def funkcija_ki_zbira_podatke(regex):
   izdelki = []
   for kategorija in kategorije:
       print(kategorija)
       for dan in datuma:  
            for i in range(1,6):
                if os.path.isfile('Novi-{}-{}-{}.html'.format(kategorija, i, dan)) == True:
                    #Yard-Garden-Outdoor-Living-stran20-26.10.2016.html
                    #print('{}-stran{}-{}.html'.format(kategorija, i, dan))
                    #deluje!!!!!!!!
                    #Zaustavijo: "Mercantile-Trades-Factories", "Other-Books", "Other-Coins-Paper-Money", "Powersports""
                    #Zaustavijo: "Bird-Supplies", "Artistic-Services", "eBay-Auction-Services", "Campground-RV-Parks"
                    #Zaustavijo: "Reward-Points-Incentives", "Test-Auctions", "Linens-Textiles-Pre-1930"
                    #Zaustavijo: "Manuscripts", "Maritime", "Other-Antiques", "Periods-Styles", "Primitives"
                    #Zaustavijo: "Rugs-Carpets", "Science-Medicine-Pre-1930", "Silver", "Direct-from-the-Artist"
                    #Zaustavijo: "Antiquarian-Collectible", "Children-Young-Adults", "Automation-Motors-Drives"
                    #Zaustavijo: "Construction", "Incunabula", "Art-from-Dealers-Resellers", "Bathing-Grooming"
                    #Zaustavijo: "Feeding", "Other-Baby", "Fiction-Literature", "Magazine-Back-Issues", "Electrical-Test-Equipment"
                    #Zaustavijo: "Heavy-Equipment", "Restaurant-Catering", "Manufacturing-Metalworking",
                    #Zaustavijo: "Other-Business-Industrial", "Retail-Services", "Lenses-Filters", "Cell-Phone-Smartphone-Parts"
                    #Zaustavijo: "Cell-Phones-Smartphones", "Coins-Canada", "Animals", "Other-Vehicles-Trailers"
                    #Upocasnijo: "Textbooks-Education", "Other-Cameras-Photo", "Textbooks-Education", "Restoration-Care", "Nonfiction" " Audiobooks"
                    #Upocasnijo: "Camera-Drone-Parts-Accs", "Dollhouse-Miniatures", "Home-Decor", "Other-Musical-Instruments"
                    #Upocasnijo: "Media-Editing-Duplication", "Cat-Supplies", "Other-Cell-Phones-Accs"
                    #Upocasnijo: "Equipment Reptile-Supplies", "Graphic-Logo-Design", "Other-Specialty-Services"
                    #Upocasnijo: "Vintage-Movie-Photography", "Video-Production-Editing"
                    if kategorija in ["Mercantile-Trades-Factories", "Other-Books", "Other-Coins-Paper-Money",
                                      "Textbooks-Education", "Other-Cameras-Photo", "Textbooks-Education", "Restoration-Care",
                                      "Nonfiction", "Audiobooks", "Camera-Drone-Parts-Accs", "Powersports", "Dollhouse-Miniatures",
                                      "Home-Decor", "Bird-Supplies", "Artistic-Services", "eBay-Auction-Services",
                                      "Other-Musical-Instruments", "Campground-RV-Parks", "Media-Editing-Duplication",
                                      "Cat-Supplies", "Other-Cell-Phones-Accs", "Reward-Points-Incentives",
                                      "Equipment Reptile-Supplies", "Graphic-Logo-Design", "Other-Specialty-Services",
                                      "Test-Auctions", "Linens-Textiles-Pre-1930", "Manuscripts", "Maritime",
                                      "Other-Antiques", "Periods-Styles", "Primitives", "Rugs-Carpets",
                                      "Science-Medicine-Pre-1930", "Silver", "Direct-from-the-Artist","Antiquarian-Collectible",
                                      "Children-Young-Adults", "Automation-Motors-Drives", "Construction",
                                      "Incunabula", "Art-from-Dealers-Resellers", "Bathing-Grooming", "Feeding",
                                      "Other-Baby", "Fiction-Literature", "Magazine-Back-Issues", "Electrical-Test-Equipment",
                                      "Heavy-Equipment", "Restaurant-Catering", "Manufacturing-Metalworking",
                                      "Other-Business-Industrial", "Retail-Services", "Lenses-Filters", "Cell-Phone-Smartphone-Parts",
                                      "Vintage-Movie-Photography", "Video-Production-Editing", "Cell-Phones-Smartphones",
                                      "Coins-Canada", "Animals", "Other-Vehicles-Trailers"]:
                        continue
                    for izdelek in re.finditer(regex, orodja.vsebina_datoteke('Novi-{}-{}-{}.html'.format(kategorija, i, dan))):
                        izdelki.append(pocisti_html(izdelek, kategorija))
                        #print(len(izdelki))
                    funkcija_da_druga_dela(izdelki)
                    print(kategorija + str(i))
                    izdelki = []
   return None

def funkcija_da_druga_dela(izdelki):
    #print('0')
    podatki = izdelki
    #print('A')
    g = open('ebay_izdelki_zmanjsano_oboje.csv', 'a')
    #print('B')
    for i in range(len(izdelki)):
        g.write(izdelki[i]['Ime'] + ',')
        g.write((izdelki[i])['Cena_Bid'] + ',')
        g.write((izdelki[i])['Bids'] + ',')
        g.write((izdelki[i])['Cena_Buy'] + ',')
        #g.write((izdelki[i])['Sold'] + ',')
        g.write((izdelki[i])['Buy'] + ',')
        g.write((izdelki[i])['Cas'] + ',')
        g.write((izdelki[i])['Drzava'] + ',')
        g.write((izdelki[i])['Kategorija'] + '\n')
    #print('Pride do sem.')
    g.close()
    podatki = []
    return None

funkcija_ki_zbira_podatke(regex_html_oboje)
#funkcija_ki_zbira_podatke(regex_html_bid)

#funkcija_ki_zbira_podatke(regex_html_buy)
##@lru_cache()
##def izloci_podatke_izdelkov(imenik):
##    izdelki = []
##    print("FUNKCIJA SE ZAGNALA")
##    for html_datoteka in orodja.datoteke(imenik):
##        print("DELUJE?")
##        for izdelek in re.finditer(regex_html, orodja.vsebina_datoteke(html_datoteka)):
##            #izdelki.append(pocisti_html(izdelek))
##            print(pocisti_html(izdelek))
##            g = open('ebay_izdelki.csv', 'w')
##            g.write(pocisti_html(izdelek)['Ime'] + ',')
##            g.write(pocisti_html(izdelek)['Cena'] + ',')
##            g.write(pocisti_html(izdelek)['Bidders'] + ',')
##            g.write(pocisti_html(izdelek)['Sold'] + ',')
##            g.write(pocisti_html(izdelek)['Now'] + ',')
##            g.write(pocisti_html(izdelek)['Cas'] + ',')
##            g.write(pocisti_html(izdelek)['Drzava'] + '\n')
##            g.close()
##            #orodja.zapisi_tabelo([pocisti_html(izdelek)], ['Ime', 'Cena', 'Bidders', 'Sold', 'Now', 'Cas', 'Drzava'], 'ebay_izdelki.csv')
##    return izdelki
##print("JA")
##izloci_podatke_izdelkov('../Strani')
#izdelki = izloci_podatke_izdelkov('../Strani')
#orodja.zapisi_tabelo(pocisti_html(izdelek), ['Ime', 'Cena', 'Bidders', 'Now', 'Sold', 'Cas', 'Drzava'], 'ebay_izdelki1.csv')
#orodja.zapisi_tabelo(izdelki, ['Ime', 'Cena', 'Bidders', 'Now', 'Shipping', 'Cas', 'Drzava'], 'ebay_izdelki.csv')





#(?P<Trusted>(Get fast shipping and excellent service when you buy from eBay Top-rated sellers)|(Get fast shipping and excellent service when you buy from eBay Top-rated sellers))?(\" />\n\s*</span>.\s*</li>.\s*</ul></li><li id=)?
