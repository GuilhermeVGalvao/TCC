#!/usr/bin/python3

import os
import subprocess
from subprocess import Popen
import json


def start(database_file='networks.json'):
    database = loaddb(database_file)["array"]
    del database[0]

    attack(database[0])
    #for network in database:
    #    attack(network)


def loaddb(file_name):
    db = {}

    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            db = json.load(file)
    else:
        raise FileNotFoundError("[*] Erro Fatal: arquivo "+file_name+" não encontrado")
    return db


def attack(net):
    #wifite = Popen(['wifite', '-b', net["bssid"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    subprocess.run(['sh', '-c', 'wifite', '-b', net["bssid"]], shell=True)