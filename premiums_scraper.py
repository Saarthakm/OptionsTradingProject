from bs4 import BeautifulSoup
import requests
from yahoo_fin import options
import csv

nflx_dates = options.get_expiration_dates("nflx")
print(nflx_dates)

with open('nflx.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(nflx_dates)
