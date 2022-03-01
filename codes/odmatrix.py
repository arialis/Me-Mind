import numpy as np
import pandas as pd
from pandas import Timestamp

class ODMatrix:

    def __init__(
            self,
            clusters,
            Users
        ):
        self.clusters = clusters
        self.Users = Users

    # crea la matrice contenente i clusters
    def create_matrix(self, clusters):
        # creo una matrice vuota che ha per righe e colonne il numero dei clusters
        matrix = np.zeros((len(clusters), len(clusters)))
        # riempio la prima riga della matrice con i clusters
        matrix[0] = clusters
        # riempio la prima colonna della matrice con i clusters
        matrix[:,0] = clusters
        return matrix

    # crea la lista dei dati per ogni utente
    def get_list(self,Users, user):
        user = Users.get_group(user)
        user_list = user.values.tolist()
        return user_list

    # controlla che la lista creata dei dati per quell'utente si possa dividere in coppie
    def pairable(self,user):
        is_pairable = False
        if len(user)>1:
            is_pairable = True
        return is_pairable

    # controlla che la lista creata dei dati per quell'utente si possa dividere in gruppi di 3 spostamenti
    def split(self,user):
        can_be = False
        if len(user)>2:
            can_be = True
        return can_be

    # divide la lista dei dati per quell'utente in coppie
    def create_pairs(self,user):   
        pairs = []
        for i in range (0, len(user)-2):
            pairs.append([user[i], user[i+1]])
        return pairs

    # divide la lista dei dati per quell'utente in coppie
    def split_in_3(self,user):   
        split = []
        for i in range (0, len(user)-2, 2):
            split.append([user[i], user[i+1], user[i+2]])
        return split

    # controlla che i movimenti degli utenti siano effettivi e non rimangano nello stesso luogo
    def check_movement(self,user):
        there_is_movement = False
        for i in range(0,len(user)):
            if user[i][0][8] != user[i][1][8]:
                there_is_movement = True
        return there_is_movement

    def get_pairing_users(self,Users):
        #lista degli spostamenti dell'utente
        pairing_users = []
        for user in Users.groups:
            user = self.get_list(Users, user) # creo la lista per ogni utente
            if(self.pairable(user)):
                pairing_users.append(self.split_in_3(user))
            else:
                continue
        return pairing_users

    def get_3_moves_users(self, Users):
        #lista degli spostamenti dell'utente
        users_3_moves = []
        for user in Users.groups:
            user = self.get_list(Users, user) # creo la lista per ogni utente
            if(self.split(user)):
                users_3_moves.append(self.create_pairs(user))
            else:
                continue
        return users_3_moves

    def get_moving_users(self, pairing_users):
        # lista degli utenti che si spostano (quindi non restano nello stesso luogo)
        moving_users = []
        for user in pairing_users:
            if(self.check_movement(user)):
                moving_users.append(user)
            else:
                continue
        return moving_users
                
    def update_matrix(self, matrix, user):
        for pair in user:
            origin = pair[0][8]
            destination = pair[1][8]
            m_columns = matrix[0].tolist()
            m_rows = matrix[:,0].tolist()
            orig_index = m_columns.index(origin)
            dest_index = m_rows.index(destination)
            matrix[orig_index][dest_index] = matrix[orig_index][dest_index] + 1
            
    def update_matrix2(self, matrix, user):
        for pair in user:
            origin = pair[0][8]
            destination = pair[1][8]
            if (origin != destination): # controllo dove c'è stato lo spostamento
                m_columns = matrix[0].tolist()
                m_rows = matrix[:,0].tolist()
                orig_index = m_columns.index(origin)
                dest_index = m_rows.index(destination)
                matrix[orig_index][dest_index] = matrix[orig_index][dest_index] + 1
            else:
                continue
