#!/usr/bin/python3

import json
import os
import re

from printer import dialog


CURRENT_PATH = os.getcwd()
LOGS_PATH = os.path.join( CURRENT_PATH, 'airodump-logs' )
DATABASE_PATH = os.path.join( LOGS_PATH, 'airodump-logs-01.csv' )
OUTPUTPATH = os.path.join( LOGS_PATH, 'airodump-logs-output.txt' )

WPS_NETWORKS_LIST = {}

def start():
    global WPS_NETWORKS_LIST
    WPS_NETWORKS_LIST = get_wps_networks_list()
    
    dialog('Gerando base de dados das redes wi-fi...')
    database = getdb()
    dialog('Base de dados gerada!')
    dialog('Organizando base de dados...')
    database = organizate(database[:])
    dialog('Base de dados organizada:')

    shortdb = []
    for i in range(0, len(database)):
        shortdb.append( database[i]["bssid"]+' '+
        database[i]["essid"]+' '+
        str(database[i]["power"])+' '+
        database[i]["privacity"])

        print( f'{database[i]["bssid"]:17}', end=' ')
        print( f'{database[i]["essid"]:32}', end=' ')
        print( f'{database[i]["power"]:6}', end=' ')
        print( f'{database[i]["privacity"]:10}', end=' ')
        print( f'{database[i]["wps"]:8}')

    dialog('Salvando base de dados...', color='orange')
    savedb(shortdb)
    savejson(database)
    dialog('Base de dados salva nos arquivos networks.txt e networks.json', color='blue')

def getdb():
    output = []

    if not os.path.exists(DATABASE_PATH):
        raise PermissionError('Você não tem permissão de execussão')

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
                "bssid": content[0].strip(),
                "channel": content[3].strip(),
                "speed": content[4],
                "privacity": content[5].strip(),
                "cipher": content[6].strip(),
                "authentication": content[7].strip(),
                "power": content[8].replace(' -', ''),
                "essid": content[13].strip()
            }
            content_json["wps"] = get_wps_from_bssid( content_json["bssid"] )
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
        

def get_wps_from_bssid(bssid):
    if bssid in WPS_NETWORKS_LIST.keys():
        return WPS_NETWORKS_LIST[bssid]
    else:
        return 'Unknown'
    

def cleanANSIcodes(text):
    ansi_remover = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    realtext = ansi_remover.sub('', text)
    return realtext


def get_wps_networks_list():
    count = -1
    index_bssid = 0
    real_index_bssid = 0
    wps_list = {}

    with open(OUTPUTPATH, 'r') as output_file:
        for line in output_file.readlines():
            count += 1
            if 'BSSID' in line:
                real_index_bssid = index_bssid
                index_bssid = count

    with open(OUTPUTPATH, 'r') as output_file:
        networks = output_file.readlines()[real_index_bssid:index_bssid]

    for line in networks:
        line = cleanANSIcodes(line)
        
        real_elements = []
        elements = line.split(' ')
        if 'Quitting' in line:
            continue

        for element in elements:
            if element != '' and element != '\n':
                real_elements.append(element)
        
        if( len(real_elements) > 0 ):
            wps_list[ real_elements[0] ] = real_elements[-1].replace('Locke\n', 'Locke')
    return wps_list