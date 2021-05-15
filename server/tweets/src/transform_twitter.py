import numpy as np
import pickle
import nltk
import urllib3
import json
from tweets.src.functions import *
from xml.etree import ElementTree
import calendar


class TransformTweets: 

    def __init__(self):
        db_conn = db_open()

        steal_words_syns = {
            "tiroteio":["tiroteio", "tiro", "bomba", "baleado", "bala", "pipoco", "perdida", "disparo"],
            "roubo": ["roubo","assalto","furto","carga","bater carteira","grupo", "tentativa","arrombamento"],
            "arrastao":["arrastao"],
            "sequestro":["sequestro"],        
            "homicidio": ["homicidio","morte", "morreu", "assassinato"],
            "outro": ["agressao","terror","trombadinha","pivete","suspeito","crime"]
        }


        reverse_map = {}
        stemming_words = []
        for key in steal_words_syns:
            for word in steal_words_syns[key]:
                stemming_words.append(word)
                reverse_map[word] = key


        stealKeywords = stemmingArray_keep_original(stemming_words)
        locality_map = readLocality()

        results = {}


        for fname in twitterTrackings:
            file = io.open("./tweets/files/"+fname+".tweets", "rb")
            tweets = pickle.load(file)
            localitys = readLocality()
            for tweet in tweets:
                words = stemmingArray(tweet.text.split(' '))
                for word in words:
                    if (word in stealKeywords):

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
                                    results[locality]["tweet"] = []
                                    results[locality]["tweet"].append({"username":tweet.user.screen_name,"date":tweet.created_at,"text":tweet.text, "type_violence": violence_type})

                                results[locality]["latlong"] = locality_map[locality]["latlong"]

                                break
                        break


        db_close(db_conn)
