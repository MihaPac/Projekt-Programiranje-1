import requests
import os
import time
import sys
timestr = time.strftime("%Y%m%d-%Hh%Mm%Ss")
timestr

#Včasih koda ne deluje, treba pognati večkrat, morda napaka v encoding.
kategorije = [
	'Asian-Antiques/20082', 'Silver/20096', 'Decorative-Arts/20086',
	'Linens-Textiles-Pre-1930/181677', 'Architectural-Garden/4707',
	'Primitives/1217', 'Maritime/37965', 'Antiquities/37903',
	'Maps-Atlases-Globes/37958', 'Periods-Styles/100927', 'Furniture/20091',
	'Rugs-Carpets/37978', 'Other-Antiques/12', 'Sewing-Pre-1930/156323',
	'Science-Medicine-Pre-1930/20094', 'Ethnographic/2207', 'Reproduction-Antiques/22608',
	'Mercantile-Trades-Factories/163091', 'Home-Hearth/163008', 'Manuscripts/23048',
	'Musical-Instruments-Pre-1930/181726'
	]
	
'''Izbral bom 20000 izdelkov iz vsake kategorije, nima vsaka kategorija 20000 izdelkov, ebay ne vraèa error message za preveliko številko strani, zato bom z regexom moral opraviti z napakami.'''

for kategorija in kategorije:
    for stran in range(1, 2):
        osnova_strani = 'http://www.ebay.com/sch/{}/i.html?_dmd=1&_sop=1&LH_Auction=1&_nkw=antiques&_pgn={}&_skc=200&rt=nc'.format(kategorija, stran)
        #Ending soonest, auction only, 200 items per page
        print(osnova_strani)
        #200 stvari na stran gledam
        url = requests.get(osnova_strani)
        cas = time.strftime("%d.%m")
        #html strani bodo imele ime dneva in meseca, na začetku vsake html datoteke bo še napisana ura, minuta, sekunda
        ime_datoteke = 'ebay-{}-stran-{:03}-'.format(kategorija, stran)+cas
        #Žal zaradi ebaya moram naenkrat shraniti vse, verjetno bom moral zbrisati duplikate.
        moja_datoteka = open(ime_datoteke + '.html', 'w')
        datoteka.write(time.strftime('%d.%m. %Hh%Mmin%Ss') + url.text)
        print('{},{}'.format(kategorija, stran))
