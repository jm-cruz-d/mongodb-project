from pymongo import MongoClient
from googleplaces import GooglePlaces, types, lang
from unidecode import unidecode 
import googlemaps
from datetime import datetime
import json
import time
import requests
import os
from dotenv import load_dotenv
load_dotenv()
import coord_amst as ca

# Searching function in API google place
def searchPlaces(query):
    API_key = os.getenv('key')
    endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    places = []
    params = {
        'query': query,
        'location': '52.37021, 4.895168',
        'radius': 5000,
        'key': API_key
    }
    res = requests.get(endpoint_url, params = params)
    results =  json.loads(res.content)
    places.extend(results['results'])
    time.sleep(2)
    while "next_page_token" in results:
        params['pagetoken'] = results['next_page_token'],
        res = requests.get(endpoint_url, params = params)
        results = json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
    return places

# Parameters search function
def getParameters(companies):
    location =[]
    for x in range(len(companies)):
        longitude = companies[x]['geometry']['location']['lng']
        latitude = companies[x]['geometry']['location']['lat']
        name=companies[x]['name']
        loc = {
            'name': name,
            'coordinates':[longitude, latitude]
        }
        location.append(loc)
    return location


starbucks = searchPlaces('Starbucks')
sbloc = getParameters(starbucks)

schools = searchPlaces('Primary school')
scloc = getParameters(schools)

kindergarten = searchPlaces('kindergarten')
kdloc = getParameters(kindergarten)

night_club = searchPlaces('night club')
ncloc = getParameters(night_club)

vegan_restaurant = searchPlaces('vegan restaurant')
vrloc = getParameters(vegan_restaurant)

airport = searchPlaces('airport amsterdam')
aloc = getParameters(airport)

db, col = ca.connectCollection('companies', 'companies')

diccsearch = {'starbucks': sbloc,
              'schools': scloc,
              'kindergarten': kdloc,
              'clubs': ncloc,
              'veganrest': vrloc,
              'airport': aloc}

# Insert collections function
def insertColl(dictionary, database):
    for k, v in dictionary.items():
        col = database[k]
        col.insert_many(v)
        print("collects inserted")

insertColl(diccsearch, db)

# Get location in each new collection
def getLocation(companies):
    location =[]
    longitude = companies['coordinates'][1]
    latitude = companies['coordinates'][0]
    loc = {
        'type':'Point',
        'coordinates':[latitude, longitude]
        }
    location.append(loc)
    print(location)
    return location

for k, v in diccsearch.items():
    for v1 in v:
        db, coll = ca.connectCollection('companies', k)
        value = {"$set": {'location':getLocation(v1)}}
        query = {"_id": v1['_id']}
        coll.update_many(query, value)