import os
import csv
from scanf import scanf
from bs4 import BeautifulSoup

# Flat structure with stat name formatted files
for folder in os.listdir("selected_stats_html"):
    path = "selected_stats_html/%s" % folder
    if os.path.isdir(path):
        for file in os.listdir(path):
            if file[0] == '.':
                continue #.DS_Store issues
            csvRows = []
            htmlFilePath = path + "/" + file
            csvDir = "selected_stats_csv_min"
            if not os.path.exists(csvDir):
                os.makedirs(csvDir)
            statYear = scanf("y%s", file.split('.')[0])[0];
            csvFilePath = csvDir + "/" + ''.join(c for c in folder if c.isalnum()) + statYear + '.csv'
            print (csvFilePath)
            if os.path.isfile(csvFilePath):
                continue
            with open(htmlFilePath, 'r', encoding='utf-8') as ff:
                f = ff.read()
                html = BeautifulSoup(f.replace('\n',''), 'html.parser')
                table = html.find('table', class_='table-styled')
                columnHeader = [t.text for t in table.find('thead').find_all('th')]
                # <player_name>, <stat_name>
                columnHeaderMin = [columnHeader[2], " ".join(folder.split())]
                csvRows.append(columnHeaderMin)
                for tr in table.find('tbody').find_all('tr'):
                    info = [td.text.replace(u'\xa0', u' ').strip() for td in tr.find_all('td')]
                    if info[2] and info[4]:
                        # <player_name (year)>, <stat>
                        infoMin = [info[2] + " (" + statYear + ")", info[4].replace(",", "")]
                        csvRows.append(infoMin)
                with open(csvFilePath, 'wt', encoding='utf-8') as csvFile:
                    writer = csv.writer(csvFile, delimiter=',')
                    for row in csvRows:
                        writer.writerow(row)
