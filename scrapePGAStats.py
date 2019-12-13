import os
import gevent
import requests
from bs4 import BeautifulSoup

statUrlFormat = "https://www.pgatour.com/stats/stat.%s.%s.html" # statId, year
categoryUrlFormat = 'https://www.pgatour.com/stats/categories.%s.html'
categoryLabels = ['ROTT_INQ', 'RAPP_INQ', 'RARG_INQ', 'RPUT_INQ', 'RSCR_INQ', 'RSTR_INQ', 'RMNY_INQ', 'RPTS_INQ']

def saveHTML(url, filename):
    print ("Saving", url, "to", filename)
    r = requests.get(url)
    with open(filename, 'wt') as f:
        f.write(r.text)

# startYear: Most recent year of stats
# numYears:  Previous # of years
def generateURL(startYear, numYears):
    statIds = []
    for category in categoryLabels:
        categoryUrl = categoryUrlFormat % (category)
        page = requests.get(categoryUrl)
        html = BeautifulSoup(page.text.replace('\n',''), 'html.parser')
        for table in html.find_all("div", class_="table-content"):
            for link in table.find_all("a"):
                statIds.append(link['href'].split('.')[1])
    for statId in statIds:
        url = statUrlFormat % (statId, startYear)
        page = requests.get(url)
        html = BeautifulSoup(page.text.replace('\n',''), 'html.parser')
        stat = html.find("div", class_="main-content-off-the-tee-details").find('h1').text
        directory = "all_stats_html/%s" % stat.replace('/', ' ') #need to replace to avoid
        if not os.path.exists(directory):
            os.makedirs(directory)
        years = []
        for option in html.find("select", class_="statistics-details-select").find_all("option"):
            year = option['value']
            if year not in years and len(years) < numYears and year != "y2020":
                years.append(year)
        urlFilenamePairs = []
        for year in years:
            url = statUrlFormat % (statId, year)
            filename = "%s/%s.html" % (directory, year)
            if not os.path.isfile(filename):
                urlFilenamePairs.append((url, filename))
        jobs = [gevent.spawn(saveHTML, pair[0], pair[1]) for pair in urlFilenamePairs]
        gevent.joinall(jobs)

# Main
generateURL("y2019", 5)
