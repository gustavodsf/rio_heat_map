import psycopg2
from datetime import datetime
from datetime import date
import calendar
import tweepy
import numpy as np
import pickle
import nltk
import csv
import re
import json
import io
import codecs
from unicodedata import normalize
import urllib3
from xml.etree import ElementTree
import traceback


'''
    Variables
'''

twitterTrackings = ['AlertaAssaltoRJ','alertario24hrs','UNIDOSPORJPA','RJ_OTT','CaosNoRio','InformeRJO','OperacoesRio','AndeSeguroApp']


def db_open():
    try:
       db_conn = psycopg2.connect("dbname='hackathon' user='postgres' host='localhost' password='postgres' port=5433")
       return db_conn
    except:
       print ("I am unable to connect to the database")
       return false


def db_close(db_conn):
    db_conn.close()

def shift(hour):
    if hour > 0 and hour < 6:
      return 'dawn'
    elif hour >=6  and hour < 12:
      return 'morning'
    elif hour >= 12 and hour < 18:
      return 'afternoon'
    else:
      return 'night'

def insert_violence(db_conn,violence):
    cur = db_conn.cursor()
    # event_data, source, lat_long
    queryStr = "INSERT INTO violence_data(latitude, longitude, event_data, neighborhood, username, type, description, address, source, day_of_week, shift) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    print (queryStr)

    try:
        print (violence['latitude'],violence["longitude"],violence["event_data"],violence["neighborhood"], violence["username"], violence["type"], violence['description'], violence['address'], violence['source'], violence['day_of_week'], violence['shift'])
        cur.execute(queryStr,(violence['latitude'],violence["longitude"],violence["event_data"],violence["neighborhood"], violence["username"], violence["type"], violence['description'], violence['address'], violence['source'], violence['day_of_week'], violence['shift']))
        db_conn.commit()
    except psycopg2.Error as e:
        print(e)
        print ("Skiping (may be because it's unique)" + violence['latitude'],violence["longitude"],violence["event_data"])
    cur.close()

def readLocality(locality_path = "./tweets/dataset/locality_ds.json" ):
    file = codecs.open(locality_path, mode="r", encoding="utf-8")
    print(file)
    text = file.read()
    locality_map = json.loads(text)

    return locality_map

def comparelocality(locality,text):
    if(locality in text):
        return True
    else:
        return False

def getLatLong(address):
    try:
        address = address.encode('utf-8')
        convertedAdress = address.decode('utf-8').replace(" ","+")
        convertedAdress = norm(convertedAdress + "+Rio+de+Janeiro")
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://nominatim.openstreetmap.org/search?q=%s&format=xml&polygon=1&addressdetails=1'%(convertedAdress));
        htmlData = str(r.data.decode('utf-8'))
        addressXmls = ElementTree.fromstring(htmlData)
        lat = float(addressXmls[0].attrib["lat"]) #Recover latitude from first address  XML response
        lon = float(addressXmls[0].attrib["lon"]) #Recover latitude from first address  XML response
        print (convertedAdress + " " + str([lat,lon]))
        return [lat,lon]
    except:
        print ("### ERROR ##")
        return None


def norm(s):
    try:
        s = normalize('NFKD', s).encode('ASCII','ignore').decode('ASCII')
    except:
        s = s.decode('utf-8')
        s = normalize('NFKD', s).encode('ASCII','ignore').decode('ASCII')
    return s

def clean_str(s):
    s = norm(s)
    s = re.sub(' ','_', s.lower() )
    s = re.sub('\W+','', s )
    return s

def readNeighborhoods(locality_path = "./tweets/dataset/localidades.csv" ):
    locality_ds = {}
    file = codecs.open(locality_path, mode="r", encoding="utf-8")
    localitys = file.readlines()
    for locality in localitys:
        key = clean_str(locality)
        if key not in locality_ds:
            locality_ds[key] = dict()
            locality_ds[key]["type"] = "neighborhood"
            locality_ds[key]["latlong"] = getLatLong(locality.strip())
            locality_ds[key]["name"] = locality.strip()

    return locality_ds

def readStreets(locality_ds,locality_path="./tweets/dataset/LinkedGeoData.csv"):
    file = codecs.open(locality_path, mode="r", encoding="utf-8")
    lines = file.readlines()
    for line in lines:
        row = line.split('\t')

        if len(row) <= 1:
            continue

        for i in range(0, len(row)):
            row[i] = row[i].replace("\n","")
            row[i] = row[i].replace("\"","")
            row[i] = row[i].strip()

        key = clean_str(row[2])
        if key not in locality_ds:
            locality_ds[key] = dict()
            locality_ds[key]["type"] = "street"
            locality_ds[key]["name"] = row[2].strip()
            if row[1] == '':
                locality_ds[key]["neighborhood"] = None
            else:
                locality_ds[key]["neighborhood"] = row[1].strip()

            if len(row) > 3:
                locality_ds[key]["latlong"] = [float(row[3]), float(row[4])]
            else:
                locality_ds[key]["latlong"] = getLatLong(row[2].strip())
    return locality_ds

def stemmingArray_keep_original(words):
    stemmer = nltk.stem.RSLPStemmer()
    stemWords = {}

    for word in words:
        word = norm(word.replace("\n","").lower())

        try:
            if(word != ""):
                stemWords[stemmer.stem(word)] = word
        except:
            print("Error in word = %s"%(word))

    return stemWords

def stemmingArray(words):
    stemmer = nltk.stem.RSLPStemmer()
    stemWords = []

    for word in words:
        word = norm(word.replace("\n","").lower())

        try:
            if(word != ""):
                stemWords.append(stemmer.stem(word))
        except:
            print("Error in word = %s"%(word))

    return stemWords

def getTypeViolence():
    conn = db_open()
    cur = conn.cursor()
    cur.execute("select name_search,id from type_violence");
    results = cur.fetchall()
    cur.close()
    return results;


class StreamTwitter(tweepy.StreamListener):

    def on_status(self, tweet):
        
        steal_words_syns = {
            "tiroteio":["tiroteio", "tiro", "bomba", "baleado", "bala", "pipoco", "perdida", "disparo"],
            "roubo": ["roubo","assalto","furto","carga","bater carteira","grupo", "tentativa","arrombamento"],
            "arrastao":["arrastao"],
            "sequestro":["sequestro"],        
            "homicidio": ["homicidio","morte", "morreu", "assassinato"],
            "outro": ["agressao","terror","trombadinha","pivete","suspeito","crime"]
        }

        
        results = {}
        reverse_map = {}
        stemming_words = []
        for key in steal_words_syns:
            for word in steal_words_syns[key]:
                stemming_words.append(word)
                reverse_map[word] = key
    
    
        stealKeywords = stemmingArray_keep_original(stemming_words)
        locality_map = readLocality()
        # print(tweet.text)
        
        words = stemmingArray(tweet.text.split(' '))
        for word in words:
            if(word in stealKeywords):
                #print("%s = %s"%(word,stealKeywords))
                #print(tweet.text)
                for locality in locality_map:
                    if(comparelocality(locality_map[locality]["name"], tweet.text)):
                        woriginal = norm(stealKeywords[word])
                        violence_type = reverse_map[woriginal]
                        stemmer = nltk.stem.RSLPStemmer()
                        id_type_violence = 13
                        for type_violence_db in getTypeViolence():                                
                            if type_violence_db[0] in steal_words_syns.keys():
                                if(violence_type in steal_words_syns[type_violence_db[0]]):
                                    id_type_violence = type_violence_db[1].__int__()
                                    break
                                

                        print ("\n####")
                        print ("Tweet: " + tweet.text)
                        print ("User: " + tweet.user.screen_name)
                        print ("Lat-long: " + str(locality_map[locality]["latlong"]))
                        print ("Detected locality: " + locality_map[locality]["name"])
                        print ("Violence Type: " + str(violence_type))
                        print ("#####\n")

                        if locality_map[locality]["type"] == "neighborhood":
                            neighborhood = locality_map[locality]["name"]
                            address = neighborhood
                        else:
                            address = (locality_map[locality]['name'] if locality_map[locality]['name'] != None  else 'Não Informado')
                            neighborhood = (locality_map[locality]['neighborhood'] if locality_map[locality]['neighborhood'] != None  else 'Não Informado')

                        if locality_map[locality]["latlong"] == None:
                            continue
                        #"type":violence_type


                        violence_json = {
                            "latitude": locality_map[locality]["latlong"][0],
                            "longitude": locality_map[locality]["latlong"][1],
                            "event_data": tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "description": tweet.text,
                            "type": id_type_violence,
                            "neighborhood": neighborhood,
                            "username": tweet.user.screen_name,
                            "address":address,
                            "source": "Twitter",
                            "shift": shift(tweet.created_at.hour),
                            "day_of_week": calendar.day_name[tweet.created_at.weekday()]
                        }
                        print(shift(tweet.created_at.hour))
                        insert_violence(db_conn,violence_json)

                        try:
                            results[locality]
                        except:
                            results[locality] = {}
                        try:
                            results[locality]["size"] += 1
                        except:
                            results[locality]["size"]  = 1

                        try:
                            results[locality]["tweet"].append({"username":tweet.user.screen_name, "date":tweet.created_at,"text":tweet.text, "type_violence": violence_type})
                        except:
                            print(word)
                            results[locality]["tweet"] = []
                            results[locality]["tweet"].append({"username":tweet.user.screen_name,"date":tweet.created_at,"text":tweet.text, "type_violence": violence_type})

                        results[locality]["latlong"] = locality_map[locality]["latlong"]

                        break
                break



