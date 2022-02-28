import numpy as np
import pandas as pd
from datetime import datetime
from pandas import Timestamp

# leggo il csv
df = pd.read_csv('../df_clusters.csv')
# elimino colonna inutile
df.drop(['Unnamed: 0'], axis='columns', inplace=True)
# converto Created_At in datetime
df['Created_At'] = pd.to_datetime(df['Created_At'])
# ordino i valori per data
df = df.sort_values(by=['Created_At'])

# crea la matrice contenente i clusters
def create_matrix(clusters):
    # creo una matrice vuota che ha per righe e colonne il numero dei clusters
    matrix = np.zeros((len(clusters), len(clusters)))
    # riempio la prima riga della matrice con i clusters
    matrix[0] = clusters
    # riempio la prima colonna della matrice con i clusters
    matrix[:,0] = clusters
    return matrix

# crea la lista dei dati per ogni utente
def get_list(Users, user):
    user = Users.get_group(user)
    user_list = user.values.tolist()
    return user_list

# controlla che la lista creata dei dati per quell'utente si possa dividere in coppie
def pairable(user):
    is_pairable = False
    if len(user)>1:
        is_pairable = True
    return is_pairable

# divide la lista dei dati per quell'utente in coppie
def create_pairs(user):   
    pairs = []
    for i in range (0, len(user)-1):
        pairs.append([user[i], user[i+1]])
    return pairs

# controlla che i movimenti degli utenti siano effettivi e non rimangano nello stesso luogo
def check_movement(user):
    there_is_movement = False
    for i in range(0,len(user)):
        if user[i][0][8] != user[i][1][8]:
            there_is_movement = True
    return there_is_movement

def get_moving_users(Users):
    #lista degli spostamenti dell'utente
    pairing_users = []
    for user in Users.groups:
        user = get_list(Users, user) # creo la lista per ogni utente
        if(pairable(user)):
            pairing_users.append(create_pairs(user))
        else:
            continue # CAMBIA E TROVA ALTERNATIVA SE NECESSARIO PER GLI UTENTI PARI
    # lista degli utenti che si spostano (quindi non restano nello stesso luogo)
    moving_users = []
    for user in pairing_users:
        if(check_movement(user)):
            moving_users.append(user)
        else:
            continue
    return moving_users

def update_matrix(matrix, user):
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

#MAIN

# raggruppo il df in base agli utenti
Users = df.groupby(['Screen_name'])

# memorizzo i clusters in una lista
clusters = df['Labels'].unique().tolist()
clusters.sort()
clusters.insert(0, None)

# creo la matrice
matrix = create_matrix(clusters)

# ottengo la lista degli utenti che compiono spostamenti 
moving_users = get_moving_users(Users)
print("In questo dataframe ci sono ", len(moving_users), "utenti che compiono spostamenti.\n")

# aggiorno la matrice quando c'è uno spostamento
for user in moving_users:
    update_matrix(matrix, user)
    
print("Matrice finale:\n")
print(matrix)


