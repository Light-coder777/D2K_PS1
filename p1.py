
from bs4 import BeautifulSoup
import requests
import os 
import os.path
import csv 
import time 
import pandas as pd

indexf = []
districtf = []
statef = []
populationf = []
growthf = []
sex_ratiof = []
literacyf = []

def writerows(rows, filename):
    with open(filename, 'a', encoding='utf-8') as toWrite:
        writer = csv.writer(toWrite)
        writer.writerows(rows)
 

def getlistings(listingurl):
    '''
    scrap footballer data from the page and write to CSV
    '''
    # prepare headers
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    # fetching the url, raising error if operation fails
    try:
        response = requests.get(listingurl, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        exit()
    soup = BeautifulSoup(response.text, "html.parser")
    listings = []
    indexl = []
    districtl = []
    statel = []
    populationl = []
    growthl = []
    sex_ratiol = []
    literacyl = []
    for rows in soup.find_all("tr"):
      try:
    
        index = rows.find("td").get_text()
        district = list(rows.find_all("td"))[1].a.get_text()
        state = list(rows.find_all("td"))[2].a.get_text()
        population = list(rows.find_all("td"))[3].get_text()
        growth = list(rows.find_all("td"))[4].get_text()
        sex_ratio = list(rows.find_all("td"))[5].get_text()
        literacy = list(rows.find_all("td"))[6].get_text()
        # print(index,district,state,population,growth, sex_ratio,literacy)
        # print(rows)
        indexl.append(index)
        districtl.append(district)
        statel.append(state)
        populationl.append(population)
        growthl.append(growth)
        sex_ratiol.append(sex_ratio)
        literacyl.append(literacy)
      except:
        print(0)
      
    return indexl,districtl,statel,populationl,growthl,sex_ratiol,literacyl

if __name__ == "__main__":
    '''
    Set CSV file name. 
    Remove if file alreay exists to ensure a fresh start
    '''
    # filename = "population.csv"
    # if os.path.exists(filename):
    #     os.remove(filename)
    
    '''
    Url to fetch consists of 3 parts:
    baseurl, page number, year, remaining url
    '''
    baseurl = "https://www.census2011.co.in/district.php?page=" 
    page = 1
    # parturl = "/sportid/24/class/2006/sort/school/starsfilter/GT/ratingfilter/GT/statuscommit/Commitments/statusuncommit/Uncommited"

    # scrap all pages
    while page < 23:
        listingurl = baseurl + str(page) 
        indexl,districtl,statel,populationl,growthl,sex_ratiol,literacyl = getlistings(listingurl)
        # getlistings(listingurl)
        indexf.extend(indexl)
        districtf.extend(districtl)
        statef.extend(statel)
        populationf.extend(populationl)
        growthf.extend(growthl)
        sex_ratiof.extend(sex_ratiol)
        literacyf.extend(literacyl)

        # take a break
        # time.sleep(3)
        page += 1


df = pd.DataFrame(list(zip(indexf,districtf,statef,populationf,growthf,sex_ratiof,literacyf)),columns =['Index','District', 'State','Population', 'Growth', 'Sex-Ratio', 'Literacy'])
print(df.tail())
df.to_csv("population_growth.csv")
if page > 1:
    print("Listings fetched successfully.")

data = pd.read_csv('population_growth.csv')
print(data.head())