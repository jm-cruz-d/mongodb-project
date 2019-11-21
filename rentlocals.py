import pandas as pd
import numpy as np
import re as re
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import folium
import googlemaps
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
import searching as se 

# Web scraping of locals rental in Amsterdam
def getPage(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

url = "http://www.dutchrental.com/commercial-property/Amsterdam"
soup = getPage(url)
rlocal = soup.select('p a')

web =[]
for r in rlocal:
    web.append(r.get('href'))

web1=[]
for i in range (2,6):
    x = getPage(f"http://www.dutchrental.com/commercial-property/Amsterdam?page={i}")   
    rlocal1 = x.select('p a')
    for r in rlocal1:
        web1.append(r.get('href'))

cleaning = web+web1
clean =[]
for c in cleaning:
    c1 = re.sub(r"/commercial-property-for-rent/Amsterdam/", "", c)
    c2 = re.sub(r"\/[0-9]+\/overview", "", c1)
    c3 = re.sub(r"\-", " ", c2)
    clean.append(c3)

# Getting coordinates with the address
gmaps = googlemaps.Client(key=os.getenv("key"))

def coordLocals(listlocals):
    addresslocals = []
    for n in listlocals:
        addresslocals.append(gmaps.places(n))      
    return addresslocals

localams = coordLocals(clean)

def getParameters(companies):
    param =[]
    for comp in companies:
        for i in range(len(comp['results'])):
            longitude = comp['results'][i]['geometry']['location']['lng']
            latitude = comp['results'][i]['geometry']['location']['lat']
            address = comp['results'][i]['name']
            loc = {
            'address': address,
            'coordinates':[longitude, latitude]
            }
            param.append(loc)
    return param

x = getParameters(localams)

# Insert collection and location for geoindex
db, coll = se.ca.connectCollection('companies', 'companies')
col = db["rentlocals"]
col.insert_many(x)

db, collr = se.ca.connectCollection('companies', 'rentlocals')

for x1 in x:
    value = {"$set": {'location':se.getLocation(x1)}}
    query = {"_id": x1['_id']}
    collr.update_many(query, value)