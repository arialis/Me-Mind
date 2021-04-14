#!/usr/bin/env python
# coding: utf-8

# ## Download and read files

# Salvo i dati in un file json con un dizionario per ogni riga dove il dizionario descrive il giorno (come nell'input), mantenendo solo i campi di interesse, ovvero:
# - text 
# - id 
# - retweeted 
# - coordinates = represents the geographic location of this Tweet as reported by the user or client application
# - timestamp_ms
# - entities 
# - retweet_count  
# - in_reply_to_user_id 
# - user 
# - geo = is it deprecated? 
# - in_reply_to_user_id_str
# - lang 
# - created_at 
# - in_reply_to_status_id_str 
# - place = when present, indicates that the tweet is associated (but not necessarily originating from) a Place

# In[4]:


import zipfile
import tarfile
import numpy as np
import json
import os
import gzip

#jupyter notebook --NotebookApp.iopub_data_rate_limit=1e10


# ### Campi non considerati:

# <li>contributors</li>
# <li>truncated</li>
# <li>is_quote_status</li>
# <li>source</li>
# <li>in_reply_to_screen_name</li>
# <li>id_str</li>
# <li>favorited</li>
# <li>filter_level</li>
# 
# Fonte: https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet

# In[2]:


#creo un unico file json con dizionari con chiave=id del tweet, valore=contenuto dei tweets

#apro la cartella zippata
tar=tarfile.open("IF-2016.tar.gz")
#salvo i file della cartella in files
files = tar.getmembers()
#creo un dizionario che conterrà i tweet per giorno    
dayDict = {}
#inizializzo i contatori
z=0
i=0

#per ogni file letto
for fileJ in files:
    name = fileJ.name
    #controllo che il file sia .json
    if name[-5:]==".json":
        #salvo il nuovo nome del file e della chiave del dizionario come 
        #"2016-09-28.json" togliendo i primi 38 caratteri dal nome del file
        day = name[38:-5]
        #creo anche un pathName per avere la directory e salvare i file
        pathName = "dataPerID.json"
        #scrivo il dizionario della giornata sul file json
        with open(pathName, 'w') as outfile:
            #estraggo il file
            with tar.extractfile(name) as f: 
                #per ogni tweet della giornata
                for jsonObj in f: 
                    #lo leggo in formato json
                    JObjDict = json.loads(jsonObj)
                    JObjDict["day"] = day
                    ID = JObjDict.get('id')
                    #faccio controlli e tolgo campi inutili
                    if 'contributors' in JObjDict:
                        JObjDict.pop('contributors')
                    if 'truncated' in JObjDict:
                        JObjDict.pop('truncated')
                    if 'source' in JObjDict:
                        JObjDict.pop('source')
                    if 'in_reply_to_screen_name' in JObjDict:
                        JObjDict.pop('in_reply_to_screen_name')
                    if 'id_str' in JObjDict:
                        JObjDict.pop('id_str')
                    if 'favorited' in JObjDict:
                        JObjDict.pop('favorited')
                    if 'filter_level' in JObjDict:
                        JObjDict.pop('filter_level')
                    if 'is_quote_status' in JObjDict:
                        JObjDict.pop('is_quote_status')
                    if 'in_reply_to_status_id' in JObjDict:
                        JObjDict.pop('in_reply_to_status_id')
                    dayDict[ID] = JObjDict
                    #incremento il contatore dei tweet
                    i+=1 
                json.dump(dayDict, outfile, indent=2)
            #incremento il contatore dei file
            z+=1
        #break #blocco per evitare troppi dati: da togliere

print('Number of tweets: ',i)
print('Number of files: ',z)


# In[5]:


#creo un file per ogni utente e ci metto dentro i contenuti dei suoi tweet andando a capo e zippo il file
listausers = []
for key, value in dayDict.items(): 
    usercontent = value['user']
    tweet = value
    json_str = '%s\n' % json.dumps(tweet)
    for k, v in usercontent.items():
        userid = usercontent["id"]
    listausers.append(userid)   
    fileout = gzip.open('uidFiles/%s.json.gz' % userid, 'a')
    fileout.write(json_str.encode('utf8'))
    fileout.close()


# ### Altre prove

# In[25]:


'''
#creo un unico file json con dizionari con chiave=giornata, valore=dizionari dei tweets

#apro la cartella zippata
tar=tarfile.open("IF-2016.tar.gz")
#salvo i file della cartella in files
files = tar.getmembers()
#creo un dizionario che conterrà i tweet per giorno    
dayDict = {}
#inizializzo i contatori
z=0
i=0

#per ogni file letto
for fileJ in files:
    name = fileJ.name
    #controllo che il file sia .json
    if name[-5:]==".json":
        dayDict = {}
        #salvo il nuovo nome del file e della chiave del dizionario come 
        #"2016-09-28.json" togliendo i primi 38 caratteri dal nome del file
        day = name[38:-5]
        #creo anche un pathName per avere la directory e salvare i file
        pathName = "dataPerDay.json"
        #scrivo il dizionario della giornata sul file json
        with open(pathName, 'w') as outfile:
            #estraggo il file
            with tar.extractfile(name) as f:
                tweetDict = {}
                #per ogni tweet della giornata
                for jsonObj in f: 
                    #creo un dizinario per ogni tweet
                    #tweetDict = {}
                    #lo leggo in formato json
                    JObjDict = json.loads(jsonObj)
                    JObjDict["day"] = day
                    ID = JObjDict.get('id')
                    #faccio controlli e tolgo campi inutili
                    if 'contributors' in JObjDict:
                        JObjDict.pop('contributors')
                    if 'truncated' in JObjDict:
                        JObjDict.pop('truncated')
                    if 'source' in JObjDict:
                        JObjDict.pop('source')
                    if 'in_reply_to_screen_name' in JObjDict:
                        JObjDict.pop('in_reply_to_screen_name')
                    if 'id_str' in JObjDict:
                        JObjDict.pop('id_str')
                    if 'favorited' in JObjDict:
                        JObjDict.pop('favorited')
                    if 'filter_level' in JObjDict:
                        JObjDict.pop('filter_level')
                    if 'is_quote_status' in JObjDict:
                        JObjDict.pop('is_quote_status')
                    if 'in_reply_to_status_id' in JObjDict:
                        JObjDict.pop('in_reply_to_status_id')
                    tweetDict[ID] = JObjDict
                    #dayDict[day].append(JObjDict)
                    #incremento il contatore dei tweet
                    i+=1 
                dayDict[day] = tweetDict
                json.dump(dayDict, outfile)
            #incremento il contatore dei file
            z+=1
        break #blocco per evitare troppi dati: da togliere

print('Number of tweets: ',i)
print('Number of files: ',z)
'''


# In[3]:


#creo tanti file json quante le giornate, in cui salvo dizionari con chiave id dei tweet e valore contenuto dei tweet
'''
#apro la cartella zippata
tar=tarfile.open("IF-2016.tar.gz")
#salvo i file della cartella in files
files = tar.getmembers()
#creo un dizionario che conterrà i tweet per giorno    
dayDict = {}
#inizializzo i contatori
z=0
i=0

#per ogni file letto
for fileJ in files:
    name = fileJ.name
    #controllo che il file sia .json
    if name[-5:]==".json":
        #salvo il nuovo nome del file e della chiave del dizionario come 
        #"2016-09-28.json" togliendo i primi 38 caratteri dal nome del file
        newName = name[38:]
        #creo anche un pathName per avere la directory e salvare i file
        pathName = "json/"+newName
        dayDict.setdefault(newName, [])
        #estraggo il file
        with tar.extractfile(name) as f: 
            #per ogni tweet della giornata
            for jsonObj in f: 
                #creo un dizinario per ogni tweet
                tweetDict = {}
                #lo leggo in formato json
                JObjDict = json.loads(jsonObj)
                #print("JObjDict = ", JObjDict)
                #se il tweet ha un id, la uso come chiave del dizionario con il contenuto del tweet
                keyJObj = JObjDict.get('id')
                if JObjDict.get('id'):
                    keyJObj = JObjDict.get('id')
                    tweetDict.setdefault(keyJObj, [])
                    #faccio controlli per eliminare campi inutili NON FUNZIONA
                    if JObjDict.get('contributors'):
                        newJObj = JObjDict.pop('contributors')
                    if JObjDict.get('truncated'):
                        JObjDict.pop('truncated')
                    if JObjDict.get('source'):
                        JObjDict.pop('source')
                    if JObjDict.get('in_reply_to_screen_name'):
                        JObjDict.pop('in_reply_to_screen_name')
                    if JObjDict.get('id_str'):
                        JObjDict.pop('id_str')
                    if JObjDict.get('favorited'):
                        JObjDict.pop('favorited')
                    if JObjDict.get('filter_level'):
                        JObjDict.pop('filter_level')
                    tweetDict[keyJObj].append(JObjDict)
                    dayDict[newName].append(tweetDict)
                else:
                    dayDict[newName].append(JObjDict)
                #appendo il dizionario con il contenuto del tweet al dizionario della giornata
                #dayDict[newName].append(tweetDict)
                #incremento il contatore dei tweet
                i+=1   
            #incremento il contatore dei file
            z+=1
        #scrivo il dizionario della giornata sul file json
        with open(pathName, 'w') as outfile:
                    json.dump(dayDict, outfile)
        break #blocco per evitare troppi dati: da togliere

print('Number of tweets: ',i)
print('Number of files: ',z)
'''


# In[11]:


'''
dict_items = dayDict.items()
#scorro la coppia valori (nome file, contenuto)
for key, value in dict_items:
    strKey = str(key)
    txtName = "texts/"+strKey[19:]
    #print(txtName)
    #apro/creo un file chiamato con il nome della giornata
    fileTxt = open(txtName,"w")
    #scorro ogni elemento del contentuto del file (ovvero ogni tweet)
    for i in range(0, len(value)):
        lista = value[i]
        fileTxt.write("{} num. {} \n\n".format("Tweet", i))
        #scorro ogni coppia di valori (indicatore, valore) di ogni tweet e li scrivo sul file
        for key2, value2 in lista.items():
            fileTxt.write("{} = {} \n".format(key2, value2))
            #print(key2, '=', value2)
        fileTxt.write("\n")
    #chiudo la lettura/scrittura del file txt    
    fileTxt.close
'''




