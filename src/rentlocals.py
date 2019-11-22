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
import functions as fun

# Web scraping of locals rental in Amsterdam
def getPage(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def main():
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
    x = fun.getLocation(localams)

    # Insert collection and location for geoindex
    db, coll = fun.connectCollection('companies', 'companies')
    col = db["rentlocals"]
    col.insert_many(x)

    print("Inserted rentlocals")

if __name__ == "__main__":
    main()