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

db, starbucks = fun.connectCollection('companies', 'starbucks')

lr = list(starbucks.find())

def counting(collection, radius):
    lst=[]
    for l in lr:
        lst.append(l['location']['coordinates'][::-1])
    data=[]
    for l in lst:
        data.append(filterType(*l,collection,radius))
    contando=[]
    for i in range(len(data)):
        contando.append(data[i].count())
    return contando


clubs = counting('clubs',250)
schools = counting('schools', 750)
veganrest = counting('veganrest', 100)
kindergarten = counting('kindergarten', 300)
amsterdam = counting('amsterdam', 250)
airport = counting('airport', 15000)

df=pd.DataFrame(lr)

def insertColumn(name, listname):
    df.insert(2, name, listname) 
    return df

insertColumn('airport', airport)
insertColumn('amsterdam', amsterdam)
insertColumn('clubs', clubs)
insertColumn('veganrest', veganrest)
insertColumn('schools', schools)
insertColumn('kindergarten', kindergarten)

headquarter = df[(df['kindergarten']>0) & (df['schools']>0) & (df['veganrest']>0) & (df['clubs']>0) & (df['amsterdam']>0) & (df['airport']>0)]
print(headquarter)