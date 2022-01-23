#!/usr/bin/python3

import os
import shutil
import subprocess
from subprocess import Popen

from printer import dialog

CURRENT_PATH = os.getcwd()
LOGS_PATH = os.path.join( CURRENT_PATH, 'airodump-logs' )

ARCHIVES_NAMES = (
    'airodump-logs-output.txt',
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

    haserror = False

    output_file = open('airodump-logs-output.txt', 'w')
    dialog('Iniciando busca por redes wi-fi...')
    airodump = Popen( ['airodump-ng', interface, '--wps', '-w', 'airodump-logs'], stdin=subprocess.PIPE, stdout=output_file, stderr=subprocess.STDOUT )
    
    if airodump.stderr != None:
        print(airodump.stderr.read().decode())
        haserror = True
    try:
        airodump.communicate(timeout=maxtimeout)
    except subprocess.TimeoutExpired as e:
        airodump.terminate()
    except KeyboardInterrupt as e:
        pass

    output_file.close()

    with open('airodump-logs-output.txt', 'r') as output_file:
        print(output_file.read())
    
    if not haserror:
        dialog('Busca terminada!')
    
    movefiles()
    


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
        dialog('Diretório não encontrado!', color='red')
        dialog('Criando novo diretório de logs...')
        os.makedirs( os.path.join(CURRENT_PATH, 'airodump-logs') )
        dialog('Novo diretório de logs criado!')
        return False


def del_oldlogs():
    for archive in ARCHIVES_NAMES:
        os.remove( os.path.join(LOGS_PATH, archive) )


def movefiles(path = LOGS_PATH, text_color='orange'):
    dialog('Salvando arquivos de log...')
    for archive in ARCHIVES_NAMES:
        try:
            dialog('Salvando', archive + '...', color=text_color)
            oldpath = os.path.join(CURRENT_PATH, archive)
            newpath = os.path.join(LOGS_PATH, archive)
            shutil.move(oldpath, newpath)
        except FileNotFoundError as e:
            dialog('Ocorreu algum erro, os arquivos de log não foram movidos', color='red')
        
    dialog('Arquivos salvos no diretório airodump-logs/', color='blue')    

