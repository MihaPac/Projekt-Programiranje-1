import os

f = open('../Kategorije/kategorije.csv', 'r')
kategorije = []
datuma = ['26.10.2016', '27.10.2016']

for line in f:
    csv_stvari = line.split(',')
    kategorije += [csv_stvari[1]]

#def naredi_csv(

csv = open('strani.csv', 'w')

for kategorija in kategorije:
    for stran in range(1, 20):
        for datum in datuma:
            datoteka = '{}-stran{:01}-{}.html'.format(kategorija, stran,
                                                      datum)
													  
			print('{}-stran{:01}-{}.html'.format(kategorija, stran,
                                                      datum))
            if os.path.isfile(datoteka) == True:
                data = open('datoteka', 'r')
                for line in data:
                    
                
                                                  
                                                  
