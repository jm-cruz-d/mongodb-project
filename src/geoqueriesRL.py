import re
import pandas as pd
from pymongo import MongoClient
import folium
import googlemaps
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
import functions as fun 

def filterType(lat,lng, typeName, radius):
    db, coll = fun.connectCollection('companies', typeName)
    results = coll.find({
        "location":{
            "$near":{
                "$geometry":{
                    "type":"Point",
                    "coordinates":[lng,lat]
                },
                "$maxDistance": radius,
            }
        }
    })
    return results

db, localrent = fun.connectCollection('companies', 'rentlocals')
lr = list(localrent.find())
    

lst=[]
def counting(collection, radius):
    for l in lr:
        lst.append(l['location']['coordinates'][::-1])
    data=[]
    for l in lst:
        data.append(filterType(*l,collection,radius))
    contando=[]
    for i in range(len(data)):
        contando.append(data[i].count())
    return contando

# Filter clubs at 1 km
clubs = counting('clubs',1000)
schools = counting('schools', 750)
starbucks = counting('starbucks',200)
veganrest = counting('veganrest', 150)
kindergarten = counting('kindergarten', 600)
amsterdam = counting('amsterdam', 750)
airport = counting('airport', 15000)

#Create a DataFrame
df=pd.DataFrame(lr)

def insertColumn(name, listname):
    df.insert(2, column=name, value=listname) 
    return df

insertColumn('airport', airport)
insertColumn('amsterdam', amsterdam)
insertColumn('clubs', clubs)
insertColumn('veganrest', veganrest)
insertColumn('starbucks', starbucks)
insertColumn('schools', schools)
insertColumn('kindergarten', kindergarten)
insertColumn('coordinates', lst)

# Cleaning a DataFrame
df=df.drop(columns=['location'])
df['address'] = df['address'].str.replace(' Parking Heinekenplein- Amsterdam -APCOA', ' ')
df['address'] = df['address'].str.replace('Parking Museum', '')
df.drop([13 , 14])
headquarter = df[(df['starbucks']>0) & (df['veganrest']>0)]

print(headquarter)