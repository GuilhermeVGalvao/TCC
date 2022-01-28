#!/usr/bin/python3

import os
import re

CURRENT_PATH = os.getcwd()
LOGS_PATH = os.path.join( CURRENT_PATH, 'airodump-logs' )
OUTPUTPATH = os.path.join( LOGS_PATH, 'airodump-logs-output.txt' )

'''
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

AIRODUMP_HAS_AN_ERROR = False
STARTING_TIME = 0

#Salva todas as redes capturadas pelo airodump em arquivos especiais na pasta
#airodump-logs
def start(interface = 'wlan0', maxtimeout=10):
    global AIRODUMP_HAS_AN_ERROR, STARTING_TIME
    STARTING_TIME = time.time()
    #checkdir()

    haserror = False

    #output_file = open('airodump-logs-output.txt', 'w')

    #airodump = subprocess.check_call( ['airodump-ng', interface, '--wps'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0 )

    dialog('Iniciando busca por redes wi-fi...', color='lb')
    airodump = Popen( ['airodump-ng', interface, '--wps'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0 )
    #stdin=subprocess.PIPE, 
    output_thread = threading.Thread(target=__show_realtime_output, args=[airodump, maxtimeout])
    
    try:
        print(airodump.returncode)
        return_code = airodump.wait(timeout=maxtimeout)

        if return_code != 0:
            dialog('ERRO DURANTE A BUSCA POR REDES:', symbol_color='lr')
            haserror = True

            for line in iter(airodump.stdout.readline, b''):
                real_line = line.decode().strip()
                dialog('    ', real_line,color='w', style='bold', symbol_color='lr')
            raise RuntimeError
        else:
            output_thread.start()
        print(airodump.returncode)


        
        airodump.terminate()
        print(airodump.returncode)

    except subprocess.TimeoutExpired as e:
        airodump.terminate()
    except KeyboardInterrupt as e:
        airodump.terminate()
    except subprocess.CalledProcessError as e:
        print(airodump.returncode)
        airodump.terminate()
        print(airodump.returncode)
    except RuntimeError as e:
        airodump.terminate()
    #output_file.close()
       
    with open('airodump-logs-output.txt', 'r') as output_file:
        if haserror:
            print()
            for line in output_file.readlines():
                new_line = cleanANSIcodes(line).strip()

                dialog('    ', new_line,color='w', style='bold', symbol_color='lr')
            print()
        else:
            print(output_file.read())
    
    if not haserror:
        dialog('Busca terminada!', color='cian')
        #movefiles()
    
    return haserror
    
    


def checkdir(path = LOGS_PATH):
    dialog('Verificando diretório de logs...')
    if os.path.isdir(path):
        dialog('Diretório encontrado', color='cian')

        has_files = False
        
        for file in ARCHIVES_NAMES:
            file_with_path = os.path.join( LOGS_PATH, file )
            if os.path.isfile(file_with_path):
                has_files = True
        
        if has_files:
            dialog('Arquivos de log antigos encontrados')
            dialog('Excluindo arquivos de log antigos...')
            del_oldlogs()
            dialog('Arquivos de log antigos apagados')
        else:
            dialog('Não foram encontrados arquivos de log antigos')
        return True
    else:
        dialog('Diretório não encontrado!', color='red')
        dialog('Criando novo diretório de logs...')
        os.makedirs( os.path.join(CURRENT_PATH, 'airodump-logs') )
        dialog('Novo diretório de logs criado!')
        return False


def del_oldlog(file_name):
    os.remove( os.path.join(LOGS_PATH, file_name) )

def del_oldlogs():
    for archive in ARCHIVES_NAMES:
        try:
            os.remove( os.path.join(LOGS_PATH, archive) )
        except FileNotFoundError as e:
            pass


def movefiles(path = LOGS_PATH, text_color='orange'):
    dialog('Salvando arquivos de log...')
    for archive in ARCHIVES_NAMES:
        try:
            oldpath = os.path.join(CURRENT_PATH, archive)
            newpath = os.path.join(LOGS_PATH, archive)
            shutil.move(oldpath, newpath)
            dialog('Salvando', archive + '...', color=text_color)
        except FileNotFoundError as e:
            dialog(f'Ocorreu algum erro, o arquivo {archive} não foi movido', color='red')
        
    dialog('Arquivos salvos no diretório airodump-logs/', color='blue')    


def __show_realtime_output(process, timeout):
    global AIRODUMP_HAS_AN_ERROR

    for line in iter(process.stdout.readline, ''):
        try:
            if time.time() >= STARTING_TIME + timeout:
                break

            if process.returncode != 0 and process.returncode != None:
                AIRODUMP_HAS_AN_ERROR = True
                break

            real_line = line.decode()
            if not real_line or real_line == '':
                continue
            sys.stdout.write(real_line)
            sys.stdout.flush()
        except KeyboardInterrupt as e:
            break


def cleanANSIcodes(text):
    ansi_remover = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    realtext = ansi_remover.sub('', text)
    return realtext

'''

'''
    airodump = Popen( ['airodump-ng', interface, '--wps'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
    
    dialog('Iniciar busca por redes? (Aperte Enter)', color='lb')
    input()

    printer = threading.Thread(target=showoutput, args=[airodump])
    printer.start()
    printer.join()


def showoutput(process):
    for line in process.stdout:  # replace '' with b'' for Python 3
        sys.stdout.write(line.decode() )
'''

'''
#!/usr/bin/python3

COLORS = {
    "purple": '\033[95m',
    "blue": '\033[94m',
    "light blue": '\033[96m',
    "cian": '\033[92m',
    "orange": '\033[93m',
    "red": '\033[91m',
    "white": '\033[0m',

    "p": '\033[95m',
    "b": '\033[94m',
    "lb": '\033[96m',
    "c": '\033[92m',
    "o": '\033[93m',
    "r": '\033[91m',
    "w": '\033[0m'
}

STYLE = {
    "default": '',
    "bold": '\033[1m',
    "underscore": '\033[4m'
}

ENDCOLOR = '\033[m'

def dialog(*msg, color='white', style='default', end='\n'):
    if color not in COLORS.keys():
        color = 'white'
    if style not in style:
        style = 'default'
    
    message = ''
    for element in msg:
        message += element + ' '
    message = message.strip()
    final_message = COLORS[color] +'[*]'+ STYLE[style] +' '+ message +' '+ ENDCOLOR

    print(final_message, end=end)

    text = '[*] ' + message
    styled_text = final_message
    return (text, styled_text)

'''