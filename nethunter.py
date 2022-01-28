#!/usr/bin/python3

import os
import sys
import re
import shutil
import time
import threading
import subprocess
from subprocess import CalledProcessError, Popen

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

STARTING_TIME = 0
SEMAPHORE = 0

#Salva todas as redes capturadas pelo airodump em arquivos especiais na pasta
#airodump-logs
def start(interface = 'wlan0', maxtimeout=10, delay=0):
    global AIRODUMP_HAS_AN_ERROR, STARTING_TIME, SEMAPHORE

    haserror = False

    dialog('Iniciando busca por redes wi-fi...', color='lb')

    airodump_is_working, error_message = airodump_test(interface)

    if not airodump_is_working:
        haserror = True

        dialog('ERRO DURANTE A BUSCA POR REDES:', symbol_color='lr')
        for line in error_message:
            if line.decode() == '' or line.decode() == '\n':
                continue
            real_line = cleanANSIcodes(line.decode())
            dialog('    ', real_line, color='w', style='bold', symbol_color='lr')

        return haserror

    
    #airodump = Popen( ['airodump-ng', interface, '--wps', '-w', 'airodump-logs'], stdin=subprocess.PIPE, stdout=output_file, stderr=subprocess.STDOUT )
    airodump = Popen( ['airodump-ng', interface, '--wps', '-w', 'airodump-logs'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0 )
    airodump_control_and_output_thread = threading.Thread(target=__show_realtime_output, args=[airodump, maxtimeout])

    try:
        STARTING_TIME = time.time()
        airodump_control_and_output_thread.start()
        SEMAPHORE = 1
        airodump_control_and_output_thread.join()
    except KeyboardInterrupt as e:
        SEMAPHORE = 0
        airodump.terminate()
        print()

    if not haserror:
        dialog('Busca terminada!', color='cian')
        checkdir(delay=delay)
        movefiles(delay=delay)
    
    return haserror
    

def checkdir(path = LOGS_PATH, delay=0):
    dialog('Verificando diretório de logs...')
    if os.path.isdir(path):
        dialog('Diretório encontrado', color='cian', delay=delay)

        has_files = False
        
        for file in ARCHIVES_NAMES:
            file_with_path = os.path.join( LOGS_PATH, file )
            if os.path.isfile(file_with_path):
                has_files = True
        
        if has_files:
            dialog('Arquivos de log antigos encontrados', delay=delay)
            dialog('Excluindo arquivos de log antigos...', delay=delay)
            del_oldlogs()
            dialog('Arquivos de log antigos apagados', delay=delay)
        else:
            dialog('Não foram encontrados arquivos de log antigos', delay=delay)
        return True
    else:
        dialog('Diretório não encontrado!', color='red', delay=delay)
        dialog('Criando novo diretório de logs...', delay=delay)
        os.makedirs( os.path.join(CURRENT_PATH, 'airodump-logs') )
        dialog('Novo diretório de logs criado!', delay=delay)
        return False


def del_oldlog(file_name):
    os.remove( os.path.join(LOGS_PATH, file_name) )

def del_oldlogs():
    for archive in ARCHIVES_NAMES:
        try:
            os.remove( os.path.join(LOGS_PATH, archive) )
        except FileNotFoundError as e:
            pass


def movefiles(path = LOGS_PATH, text_color='orange', delay=0):
    dialog('Salvando arquivos de log...')
    for archive in ARCHIVES_NAMES:
        try:
            dialog('Salvando', archive + '...', color=text_color, delay=delay)
            oldpath = os.path.join(CURRENT_PATH, archive)
            newpath = os.path.join(LOGS_PATH, archive)
            shutil.move(oldpath, newpath)
        except FileNotFoundError as e:
            dialog('Ocorreu algum erro, os arquivos de log não foram movidos', color='red', delay=delay)
        
    dialog('Arquivos salvos no diretório airodump-logs/', color='blue', delay=delay)


def airodump_test(interface):
    airodump = Popen( ['airodump-ng', interface, '--wps'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0 )
    try:
        err = airodump.communicate(timeout=4)[0].split(b'\n')

        airodump.terminate()
        return False, err
    except subprocess.TimeoutExpired as e:
        airodump.terminate()
        return True, None


def __show_realtime_output(process, timeout):
    '''Mostra a saída de um subprocesso e o encerra após o timeout 

    Parameters
    ----------
    Args:
        process (Popen)
        timeout (int) : Se timeout = None, então a
        execusão será infinita até que o usuário
        decida parar usando CTRL + C 
    '''
    global SEMAPHORE

    with open('airodump-logs-output.txt', 'w') as output_file:
        output_file.write('')
    
    with open('airodump-logs-output.txt', 'a') as output_file:
        for line in process.stdout:
            try:
                if timeout is not None:
                    if time.time() >= STARTING_TIME + timeout:
                        process.terminate()
                        break
                if SEMAPHORE == 0:
                    process.terminate()
                    break

                real_line = line.decode()
                if not real_line or real_line == '':
                    continue

                output_file.write(real_line)

                sys.stdout.write(real_line)
                sys.stdout.flush()
            except KeyboardInterrupt as e:
                print('Foi')
                break


def cleanANSIcodes(text):
    ansi_remover = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    realtext = ansi_remover.sub('', text)
    return realtext
