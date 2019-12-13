import os
import csv
import gevent
import json
import requests
from bs4 import BeautifulSoup

playerUrlFormat = "https://www.pgatour.com/players/player.%s.%s.html" # playerId, player-name-url
playerProfilesCSV = "player_profiles/playerProfiles.csv"

def writeProfile(url, filename):
    print ("Saving", url, "to", filename)
    r = requests.get(url)
    with open(filename, 'wt') as f:
        f.write(r.text)

# startYear: Most recent year of stats
# numYears:  Previous # of years
def generateURL():
    selectedPlayers = []
    p = json.load(open('player_profiles/players.json'))
    with open('player_profiles/selectedPlayers.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            for player in p['players']:
                if player['name'] == row[0]:
                    playerInfo = [player['name'], player['country'], playerUrlFormat % (player['id'], player['urlName'])]
                    selectedPlayers.append(playerInfo)
                    print ('Added ', playerInfo)
                    break

    csvRows = []
    csvRows.append(['PLAYER NAME', 'Country', 'College'])
    for playerInfo in selectedPlayers:
        url = playerInfo[2]
        page = requests.get(url)
        html = BeautifulSoup(page.text.replace('\n',''), 'html.parser')
        profile = html.find("div", class_="player-profile-module")
        rowInfo = []
        if profile:
            for profileStat in profile.find_all("div", class_="s-col__row"):
                if profileStat.find("p", class_="s-bottom-text").text == "College":
                    if profileStat.find("p", class_="s-top-text").text:
                        rowInfo = [playerInfo[0], playerInfo[1], profileStat.find("p", class_="s-top-text").text]
                    else:
                        rowInfo = [playerInfo[0], playerInfo[1], ""]
                    print (rowInfo)
                    break
            if not rowInfo:
                rowInfo = [playerInfo[0], playerInfo[1], ""]
                print (rowInfo)
        else:
            rowInfo = [playerInfo[0], playerInfo[1], ""]
            print (rowInfo)
        csvRows.append(rowInfo)

    with open(playerProfilesCSV, 'wt', encoding='utf-8') as outputCSVFile:
        writer = csv.writer(outputCSVFile, delimiter=',')
        for row in csvRows:
            writer.writerow(row)

        #for year in years:
        #   url = statUrlFormat % (statId, year)
        #    filename = "%s/%s.html" % (directory, year)
        #    if not os.path.isfile(filename):
        #        urlFilenamePairs.append((url, filename))
        #jobs = [gevent.spawn(saveHTML, pair[0], pair[1]) for pair in urlFilenamePairs]
        #gevent.joinall(jobs)

# Main
generateURL()
