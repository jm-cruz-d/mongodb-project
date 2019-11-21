from pymongo import MongoClient
import folium
import googlemaps
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll


def getLocation(companies):
    param =[]
    for comp in companies:
        for i in range(len(comp['results'])):
            longitude = comp['results'][i]['geometry']['location']['lng']
            latitude = comp['results'][i]['geometry']['location']['lat']
            address = comp['results'][i]['name']
            loc = {
            'address': address,
            'location':{
                'type':'Point',
                'coordinates':[longitude, latitude]
                       }
            }
            param.append(loc)
    return param