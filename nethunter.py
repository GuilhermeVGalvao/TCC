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

verbose = False

#Salva todas as redes capturadas pelo airodump em arquivos especiais na pasta
#airodump-logs
def start(interface = 'wlan0', maxtimeout=10, useverbose=False):
    global verbose
    verbose = useverbose

    checkdir()

    try:
        dialog('Iniciando busca por redes wi-fi...')
        airodump = Popen( ['airodump-ng', interface, '-w', 'airodump-logs'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True )
        global output
        airodump.communicate(timeout=maxtimeout)
    except subprocess.TimeoutExpired as e:
        dialog('Busca terminada!')
        airodump.send_signal(15)
        dialog('Salvando arquivos de log...')
        movefiles()
        dialog('Arquivos salvos no diretório airodump-logs/')


def checkdir(path = LOGS_PATH):
    dialog('Verificando diretório de logs...')
    if os.path.isdir(path):
        dialog('Diretório encontrado')
        try:
            dialog('Arquivos de log antigos foram encontrados')
            dialog('Apagando arquivos de log antigos...')
            del_oldlogs()
            dialog('Arquivos de log antigos apagados')
        except FileNotFoundError as e:
            dialog('Não foram encontrados arquivos de log antigos')
        return True
    else:
        dialog('Diretório não encontrado!')
        dialog('Criando novo diretório de logs...')
        os.makedirs( os.path.join(CURRENT_PATH, 'airodump-logs') )
        dialog('Novo diretório de logs criado!')
        return False


def del_oldlogs():
    for archive in ARCHIVES_NAMES:
        os.remove( os.path.join(LOGS_PATH, archive) )


def movefiles(path = LOGS_PATH):
    for archive in ARCHIVES_NAMES:
        dialog('Salvando', archive + '...')
        oldpath = os.path.join(CURRENT_PATH, archive)
        newpath = os.path.join(LOGS_PATH, archive)
        shutil.move(oldpath, newpath)


def dialog(*msg):
    if verbose == True:
        print('[*]', *msg)