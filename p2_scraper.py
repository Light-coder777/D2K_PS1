from bs4 import BeautifulSoup
import requests
import os 
import os.path
import csv 
import time 
import pandas as pd

baseurl = "https://primeinvestor.in/nifty-50-returns/" 
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
# fetching the url, raising error if operation fails
try:
    response = requests.get(baseurl, headers=headers)
except requests.exceptions.RequestException as e:
    print(e)
    exit()
soup = BeautifulSoup(response.text, "html.parser")

# print(soup.find_all("tr"))