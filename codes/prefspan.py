from datetime import datetime
import pandas as pd
from pandas import Timestamp
from prefixspan import PrefixSpan

class PSpan:

    def __init__(
            self,
            df
        ):
        self.df = df

    # definisco la funzione per ottenere la lista con i 3 frequent patterns a partire dal dataframe
    def ps3(self, df):
        # raggruppo il df in base agli utenti
        Users = df.groupby(['Screen_name'])
        lista = []
        # aggiungo alla lista le sequenze di cluster lables per utente
        for group in Users:
            user = []
            if 'Labels' in df:
                for label in group[1]['Labels']:
                    user.append(label)
                lista.append(user)
            elif 'geohash' in df:
                for label in group[1]['geohash']:
                    user.append(label)
                lista.append(user)
        # preparo l'algoritmo PrefixSpan con frequenza 3 e closed
        ps = PrefixSpan(lista)
        ps = ps.frequent(3, closed=True)
        # aggiungo alla lista frequent_moves solo quelli con almeno 3 spostamenti
        frequent_moves = []
        for item in ps:
            if(len(item[1])>2):
                frequent_moves.append(item)
        frequent_moves.sort(reverse=True)
        return frequent_moves
