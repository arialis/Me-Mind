import zipfile
import tarfile as tar
import numpy as np
import json
import os
import gzip as gz
from pathlib import Path

class ReadData:

    def __init__(
            self,
            tar,
            tarfiles,
            pathName,
            UID,
            tweetDictionary,
        ):
        self.tar = tar,
        self.tarfiles = tarfiles,
        self.pathName = pathName,
        self.UID = UID,
        self.tweetDictionary = tweetDictionary
    
    def dataPerID(self, tar, tarfiles, pathName, tweetDictionary):
        #inizializzo i contatori
        z=0 #contatore files
        i=0 #contatore tweets
        #per ogni file letto
        for fileExctracted in tarfiles:
            fileName = fileExctracted.name
            #controllo che il file sia .json o .gz SISTEMA QUESTA PARTE!!!!!!!!!
            if fileName.endswith('json.gz'):
                f = gz.open('../tar_files/'+fileName, "rb")
                fileName = f.name
            if fileName.endswith('.json'):
                #salvo il nuovo nome del file e della chiave del dizionario come 
                #"2016-09-28.json" togliendo i primi 38 caratteri dal nome del file
                day = fileName[38:-5]
                #scrivo il dizionario della giornata sul file json
                with open(pathName, 'a') as outfile:
                    #estraggo il file
                    with tar.extractfile(fileName) as f: 
                        #per ogni tweet della giornata
                        for jsonObj in f: 
                            #lo leggo in formato json
                            JObjDict = json.loads(jsonObj)
                            JObjDict["day"] = day
                            ID = JObjDict.get('id') # prendo l'id del tweet come chiave da usare nel dizionario
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
                            tweetDictionary[ID] = JObjDict
                            #incremento il contatore dei tweet
                            i+=1 
                        json.dump(tweetDictionary, outfile, indent=2)
                    #incremento il contatore dei file
                    z+=1
        print('Number of tweets: ',i)
        print('Number of files: ',z)
        return tweetDictionary

    #creo un file per ogni utente e ci metto dentro i contenuti dei suoi tweet andando a capo e zippo il file
    def createUIDFiles(self, UID, tweetDictionary):
        listaUsers = []
        UID_dir = '../'+UID
        if(os.path.isdir(UID_dir)) == False: 
            os.mkdir(UID_dir)
        for key, value in tweetDictionary.items(): #scorro ogni elemento del dizionario formato da {ID tweet: contenuti}
            usercontent = value['user'] # contents del campo user per quel tweet
            tweet = value # è il tweet ovvero il value precedente (tutto il contenuto)
            userid = usercontent['id'] #salvo l'id utente
            if userid in listaUsers:
                continue
            else:
                userTweets = []
                for key2, value2 in tweetDictionary.items():
                    usercontent2 = value2['user']
                    tweet2 = value2
                    userid2 = usercontent2['id']
                    if userid2 == userid:
                        userTweets.append(tweet2)
                    else:
                        continue
                listaUsers.append(userid)   
                fileout = gz.open(UID_dir+'/%s.json.gz' % userid, 'w')
                json_str = '%s\n' % json.dumps(userTweets) # contenuto del tweet in formato json
                fileout.write(json_str.encode('utf8'))
                fileout.close()

    