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

db, coll = connectCollection('companies', 'companies')


# Query in companies collection.
alloffices = [
    {"$unwind": "$offices"},
    {"$match":{"$and": [{"offices.city": "Amsterdam"}, {'deadpooled_year':None}]}}]

comp = list(coll.aggregate(alloffices))

# Function that generates a list of offices with latitude and longitude nulls, 
# other list with the succesfull offices and other with latitude and longitude wrongs.
def outNulls(company):
    ll_null = []
    ll=[]
    strange = []
    for x in range(len(company)): 
        if company[x]['offices']['longitude']==None or company[x]['offices']['latitude']==None:
            if company[x]['offices']['address1'] != "" or company[x]['offices']['address2'] != "":         
                ll_null.append(company[x])
        elif company[x]['offices']['latitude'] > 50:
            ll.append(company[x])
        else:
            strange.append(company[x])
            
    return ll_null, ll, strange

lnulls, lwith, lstrg = outNulls(comp)

# Connection with googlemaps API
gmaps = googlemaps.Client(key=os.getenv("key"))

# Function that generates coordinates in the nulls list with the adress and the google API
def coordNews(listcompanies):
    datnew = []
    llnew = []
    for n in listcompanies:
        if n['offices']['address1'] != '':
            datnew.append(gmaps.places(n['offices']['address1']))
        elif n['offices']['address2'] != '':
            datnew.append(gmaps.places(n['offices']['address2']))
    for x in range(len(datnew)):
            for i in range(len(datnew[x]['results'])):
                llnew.append(datnew[x]['results'][i]['geometry']['location'])
    return llnew

xll = coordNews(lnulls)

# Changes nulls coordinates in the dictionary with the new coordinates of above function
def changeKeys(dict1, dict2):
    for x in range(len(dict1)):
        dict1[x]['offices']['longitude'] = xll[x]['lng']
        dict1[x]['offices']['latitude'] = xll[x]['lat']
    return dict1

notnulls = changeKeys(lnulls, xll)
strll = coordNews(lstrg)
newstr = changeKeys(lstrg, strll)

# Create a new list with all the offices
amsterdam = lwith + notnulls + newstr

# Insert new collection
col = db['amsterdam']
col.insert_many(amsterdam)

print(db.list_collection_names())

db, coll2 = connectCollection('companies', 'amsterdam')

# Insert location to create geoindex
def getLocation(companies):
    location =[]
    longitude = companies['offices']['longitude']
    latitude = companies['offices']['latitude']
    loc = {
        'type':'Point',
        'coordinates':[float(longitude), float(latitude)]
    }
    location.append(loc)
    return location

for cp in amsterdam:
    value = {"$set": {'location':getLocation(cp)}}
    query = {"_id": cp['_id']}
    coll2.update_many(query, value)

comp2 = list(coll2.find({"funding_rounds.raised_amount": {"$gte": 1000000}}))