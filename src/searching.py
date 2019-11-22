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

# Parameters search function and location
def getLocation(companies):
    location =[]
    for x in range(len(companies)):
        longitude = companies[x]['geometry']['location']['lng']
        latitude = companies[x]['geometry']['location']['lat']
        name=companies[x]['name']
        address=companies[x]['formatted_address']
        loc = {
            'name': name,
            'address': address,
            'location':{
                'type':'Point',
                'coordinates':[longitude, latitude]
                       }
        }
        location.append(loc)
    return location


starbucks = searchPlaces('Starbucks')
sbloc = getLocation(starbucks)

schools = searchPlaces('Primary school')
scloc = getLocation(schools)

kindergarten = searchPlaces('kindergarten')
kdloc = getLocation(kindergarten)

night_club = searchPlaces('night club')
ncloc = getLocation(night_club)

vegan_restaurant = searchPlaces('vegan restaurant')
vrloc = getLocation(vegan_restaurant)

airport = searchPlaces('airport amsterdam')
aloc = getLocation(airport)

shops = searchPlaces('coffee shop')
shoploc = getLocation(shops)

db, col = ca.connectCollection('companies', 'companies')

diccsearch = {'coffeeshop': shoploc,
              'starbucks': sbloc,
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
