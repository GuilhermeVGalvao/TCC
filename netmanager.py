#!/usr/bin/python3

import json
import os

CURRENT_PATH = os.getcwd()
LOGS_PATH = os.path.join( CURRENT_PATH, 'airodump-logs' )
DATABASE_PATH = os.path.join( LOGS_PATH, 'airodump-logs-01.csv' )

def start():
    print('[*] Gerando base de dados das redes wi-fi...')
    database = getdb()
    print('[*] Base de dados gerada!')
    print('[*] Organizando base de dados...')
    database = organizate(database[:])
    print('[*] Base de dados organizada:')

    shortdb = []
    for i in range(0, len(database)):
        shortdb.append( database[i]["bssid"]+
        database[i]["essid"]+' '+
        str(database[i]["power"])+
        database[i]["privacity"])

        print( f'{database[i]["bssid"]:17}', end=' ')
        print( f'{database[i]["essid"]:32}', end=' ')
        print( f'{database[i]["power"]:6}', end=' ')
        print( f'{database[i]["privacity"]:8}')

    print('[*] Salvando base de dados...')
    savedb(shortdb)
    savejson(database)
    print('[*] Base de dados salva nos arquivos networks.txt e networks.json')

def getdb():
    output = []
    with open(DATABASE_PATH, 'r') as file:
        cont = 0
        for line in file:
            content = line.split(',')

            if line == '\n':
                cont += 1
                continue
            if cont >= 2:
                break
            if content[13] == ' ':
                continue
            
            content_json = {
                "bssid": content[0],
                "channel": content[3],
                "speed": content[4],
                "privacity": content[5],
                "cipher": content[6],
                "authentication": content[7],
                "power": content[8].replace(' -', ''),
                "essid": content[13]
            }
            output.append(content_json)
    for i in range(1, len(output) ):
        output[i]["speed"] = int(output[i]["speed"])
        output[i]["power"] = int(output[i]["power"])
    return output[:]


def organizate(array):
    new_array = []
    while True:
        bigger = 0
        index = 0
        for i in range( 1, len(array) ):
            if array[i]["power"] >= bigger:
                bigger = array[i]["power"]
                index = i
        new_array.append(array[index])
        array.pop(index)

        if len(array) == 1:
            new_array.insert(0, array[0])
            break
    return new_array[:]


def savedb(array):
    with open('networks.txt', 'w') as file:
        file.write('')
    with open('networks.txt', 'a') as file:
        for i in range(1, len(array)):
            file.write(array[i] + ' \n')


def savejson(array):
    obj = {
        "array": array
    }
    with open('networks.json', 'w') as file:
        json.dump(obj, file, indent=3)
        
