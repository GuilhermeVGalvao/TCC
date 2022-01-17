import os

import os
CURRENT_PATH = os.getcwd()
LOGS_PATH = os.path.join( CURRENT_PATH, 'airodump-logs' )
DATABASE_PATH = os.path.join( LOGS_PATH, 'airodump-logs-01.csv' )

def start():
    database = getdb()
    
    for i in range(0, len(database)):
        print( f'{database[i]["bssid"]:17}', end=' ')
        print( f'{database[i]["essid"]:32}', end=' ')
        print( f'{database[i]["power"]:6}', end=' ')
        print( f'{database[i]["privacity"]:8}')


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
                "power": content[8].replace('-', ''),
                "essid": content[13]
            }
            output.append(content_json)
    
    return output[:]

            