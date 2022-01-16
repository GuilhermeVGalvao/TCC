#!/usr/bin/python3

import os
import shutil
import subprocess
from subprocess import Popen

CURRENT_PATH = os.getcwd()
LOGS_PATH = os.path.join( CURRENT_PATH, 'airodump-logs' )

ARCHIVES_NAMES = (
    'airodump-logs-01.cap',
    'airodump-logs-01.csv',
    'airodump-logs-01.kismet.csv',
    'airodump-logs-01.kismet.netxml',
    'airodump-logs-01.log.csv'
)

#Salva todas as redes capturadas pelo airodump em arquivos especiais na pasta
#airodump-logs
def start(interface = 'wlan0', maxtimeout=10):
    checkdir()

    try:
        airodump = Popen( ['airodump-ng', interface, '-w', 'airodump-logs'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True )
        output, errors = airodump.communicate(timeout=maxtimeout)
    except subprocess.TimeoutExpired as e:
        airodump.send_signal(15)
        #movefiles()


def checkdir(path = LOGS_PATH):
    if os.path.isdir(path):
        try:
            os.remove( os.path.join(path, 'airodump-logs-01.cap') )
            os.remove( os.path.join(path, 'airodump-logs-01.csv') )
            os.remove( os.path.join(path, 'airodump-logs-01.kismet.csv') )
            os.remove( os.path.join(path, 'airodump-logs-01.kismet.netxml') )
            os.remove( os.path.join(path, 'airodump-logs-01.log.csv') )
            print('[*] Arquivos de log antigos foram apagados')
        except Exception as e:
            print('[*] Não há arquivos de log antigos para limpeza')
        return True
    else:
        os.makedirs( os.path.join(CURRENT_PATH, 'airodump-logs') )
        return False


def movefiles(path = LOGS_PATH):
    checkdir()
    for archive in ARCHIVES_NAMES:
        oldpath = os.path.join(CURRENT_PATH, archive)
        newpath = os.path.join(LOGS_PATH, archive)
        shutil.move(oldpath, newpath)
    