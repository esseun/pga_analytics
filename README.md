# Analysis of PGA Tour Statistics
Scripts written as part of Data Analytics Project for GSBA505B STATS at the Marshall School of Business OMBA Program (University of Southern California).  
This repository contains python scripts used for initial data scraping of pgatour.com.  
Analysis results as well as SAS Programs (data joins) available on: Work in Progress

## Software Requirements
- Python 3.6 (pip)
- Beautiful Soup 4+
- gevent
- requests
- csv

## Getting Started
### Data Collection
`python3.6 scrapePGAStats.py`  
   Scrapes pgatour.com for all stats from 2015-2019 (configurable in generateURL call) and generates html files into all_stats_html/ folder. Copy select folders of interest in all_stats_html/ into the selected_stats_html/ folder for CSV conversion.  

`python3.6 convertToCSV.py`  
   Converts html files in selected_stats_html/ folder to CSV files AS IS into selected_stats_csv  

`python3.6 convertToCSVFlat.py`  
   Converts html files in selected_stats_html/ folder into two column (Player Name, Stat) CSV files into selected_stats_csv_min\ folder  

`python3.6 scrapePlayerProfiles.py`  
   Scrapes pgatour.com for Country and College fields for all players listed in player_profiles/playerProfiles.csv  
