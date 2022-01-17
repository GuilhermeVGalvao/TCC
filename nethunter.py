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
        print('[*] Iniciando busca por redes wi-fi...')
        airodump = Popen( ['airodump-ng', interface, '-w', 'airodump-logs'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True )
        global output
        airodump.communicate(timeout=maxtimeout)
    except subprocess.TimeoutExpired as e:
        print('[*] Busca terminada!')
        airodump.send_signal(15)
        print('[*] Salvando arquivos de log...')
        movefiles()
        print('[*] Arquivos salvos no diretório airodump-logs/')


def checkdir(path = LOGS_PATH):
    print('[*] Verificando diretório de logs...')
    if os.path.isdir(path):
        print('[*] Diretório encontrado')
        try:
            print('[*] Arquivos de log antigos foram encontrados')
            print('[*] Apagando arquivos de log antigos...')
            del_oldlogs()
            print('[*] Arquivos de log antigos apagados')
        except FileNotFoundError as e:
            print('[*] Não foram encontrados arquivos de log antigos')
        return True
    else:
        print('[*] Diretório não encontrado!')
        print('[*] Criando novo diretório de logs...')
        os.makedirs( os.path.join(CURRENT_PATH, 'airodump-logs') )
        print('[*] Novo diretório de logs criado!')
        return False


def del_oldlogs():
    for archive in ARCHIVES_NAMES:
        os.remove( os.path.join(LOGS_PATH, archive) )


def movefiles(path = LOGS_PATH):
    for archive in ARCHIVES_NAMES:
        print('[*] Salvando', archive + '...')
        oldpath = os.path.join(CURRENT_PATH, archive)
        newpath = os.path.join(LOGS_PATH, archive)
        shutil.move(oldpath, newpath)
    