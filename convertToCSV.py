import os
import csv
from bs4 import BeautifulSoup

# Retain folder structure
for folder in os.listdir("selected_stats_html"):
    path = "selected_stats_html/%s" % folder
    if os.path.isdir(path):
        for file in os.listdir(path):
            if file[0] == '.':
                continue #.DS_Store issues
            csvRows = []
            htmlFilePath = path + "/" + file
            csvDir = "selected_stats_csv/" + folder
            if not os.path.exists(csvDir):
                os.makedirs(csvDir)
            csvFilePath = csvDir + "/" + file.split('.')[0] + '.csv'
            print (csvFilePath)
            if os.path.isfile(csvFilePath):
                continue
            with open(htmlFilePath, 'r') as ff:
                f = ff.read()
                html = BeautifulSoup(f.replace('\n',''), 'html.parser')
                table = html.find('table', class_='table-styled')
                columnHeader = [t.text for t in table.find('thead').find_all('th')]
                csvRows.append(columnHeader)
                for tr in table.find('tbody').find_all('tr'):
                    info = [td.text.replace(u'\xa0', u' ').strip() for td in tr.find_all('td')]
                    csvRows.append(info)
                with open(csvFilePath, 'wt') as csvFile:
                    writer = csv.writer(csvFile, delimiter=',')
                    for row in csvRows:
                        writer.writerow(row)
