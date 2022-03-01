import numpy as np
import json
import os
import gzip as gz
from shapely.geometry import *
import pandas as pd
from pandas import DataFrame 

class CreateDF:

    def __init__(
            self,
            entries, 
            df, 
            folder_name, 
            fileWithCoord,
            coords
        ):
        self.entries = entries,
        self.df = df,
        self.folder_name = folder_name,
        self.fileWithCoord = fileWithCoord,
        self.coords = coords

    def createFilesWithCoord(self, entries, folder_name, fileWithCoord):
            #creo la lista dei file con le coordinate diverse da null
            for entry in entries:
                entry_name = os.path.basename(entry)
                if entry_name.endswith('.json.gz'):
                    file = gz.open('../'+folder_name+'/'+entry, "rb")
                    for jsonObj in file:
                        jsonRead = json.loads(jsonObj)
                        for item in jsonRead:
                            if 'coordinates' in item:
                                if str(item['coordinates']) == 'None': 
                                    continue
                                else:
                                    if entry_name not in fileWithCoord: #controllo che il file non sia già nella lista
                                        fileWithCoord.append(entry)
            return fileWithCoord     

    def createDf(self, entries, df, folder_name, fileWithCoord, coords):
        for entry in entries:
            entry_name = os.path.basename(entry)
            if entry_name in fileWithCoord:
                file = gz.open('../'+folder_name+'/'+entry, "rb")
                for jsonObj in file:
                    jsonRead = json.loads(jsonObj)
                    for item in jsonRead:
                        usercontent = item['user']
                        creation = item['created_at']
                        userID = usercontent['id']
                        screen_name = usercontent['screen_name']
                        tweetID = item['id']
                        txt = item['text']
                        geo = item['geo']
                        if str(item['geo']) != 'None':
                            coordinates = item['geo']
                            pointCoordinates = Point(coordinates['coordinates']) #creo il punto per ogni set di coordinate
                            if (pointCoordinates.within(coords)): #controllo se il punto è nell'area di Pisa
                                lat = pointCoordinates.x
                                lon = pointCoordinates.y
                                new_row = pd.Series(data={'Screen_name':screen_name, 'UserID':userID, 'TweetID':tweetID, 'Coords':[float(lat)]+[float(lon)], 'Lat':lat, 'Lon':lon, 'Created_At':creation, 'Text':txt}, name='x')
                                df = df.append(new_row) #append row to the dataframe
        return df