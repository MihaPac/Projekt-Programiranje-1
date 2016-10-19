import requests
import os
import time
import sys

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

'''Izbral bom 20000 izdelkov iz vsake kategorije, nima vsaka kategorija 20000 izdelkov, ebay ne vrača error message za preveliko številko strani, zato bom z regexom moral opraviti z napakami.'''

print("Vtipkaj 'zajem_vseh_strani(število)', da bo program dol potegnil vso informacijo. (Priporočam vsaj 20 in manj kot 100)")

def naredi_datoteko(datoteka):
	os.makedirs(os.path.dirname(datoteka))
#	with open(datoteka, "w") as f:
#		f.write("FOOBAR")
#Ta koda vzeta direkt od http://stackoverflow.com/questions/12517451/python-automatically-creating-directories-with-file-output

def zajem_vseh_strani(do_kod):
	for kategorija in kategorije:
		for stran in range(1, do_kod):
			osnova_strani = 'http://www.ebay.com/sch/{}/i.html?_dmd=1&_sop=1&LH_Auction=1&_nkw=antiques&_pgn={}&_skc=200&rt=nc'.format(kategorija, stran)
			#Ending soonest, auction only, 200 items per page
			url = requests.get(osnova_strani)
			cas = time.strftime("%d.%m")
			#html strani bodo imele ime dneva in meseca, na začetku vsake html datoteke bo že napisana ura, minuta, sekunda
			ime_datoteke = 'ebay-{}-stran-{:03}-'.format(kategorija, stran) + cas
			#Žal zaradi ebaya moram naenkrat shraniti vse, verjetno bom moral zbrisati duplikate.
			datoteka = "/Ebay, dneva " + time.strftime("Ebay, dneva %d.%m.")
			moja_datoteka = open(datoteka + ime_datoteke + '.html', 'w')
			naredi_datoteko(moja_datoteka)
			datoteka.write(time.strftime('%d.%m. %Hh%Mmin%Ss') + url.text)
			print('{},{}'.format(kategorija, stran))

zajem_vseh_strani(2)
