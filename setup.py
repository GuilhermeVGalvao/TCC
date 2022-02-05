#!/usr/bin/python3

import os
import sys
from printer import dialog

CURRENT_PATH = os.getcwd()
INSTALL = False

def main():
    global CURRENT_PATH, INSTALL

    lr = '\033[31m'

    if not os.getuid() == 0:
        sys.exit(f'{lr}[*] O Setup deve ser executado como superusuário!')
    
    dialog('Atualizando repositórios do sistema...', color='blue')
    os.system('apt-get update -y')
    print('')

    dialog('Instalando Python3...', color='blue')
    os.system('apt-get install -y python3')
    print('')

    dialog('Instalando pip3...', color='blue')
    os.system('apt-get install -y pip3')
    print('')

    dialog('Instalando git...', color='blue')
    os.system('apt-get install -y git')
    print('')

    dialog('Instalando aircrack-ng...', color='blue')
    os.system('apt-get install -y aircrack-ng')
    print('')

    dialog('Instalando Wifite...', color='blue')
    os.system('apt-get install -y wifite')
    print('')

    dialog('Instalando dependências do Wifite...', color='blue')
    os.system('pip3 install pytest-flake8')
    print('')

    while True:
        dialog('Você gostaria de instalar o Wihunter no sistema? [S/N]', color='blue')
        dialog('(assim poderá usá-lo diretamente como um comando)', color='blue')
        answer = input('>> ').upper()

        if answer == 'S':
            INSTALL = True
            break
        elif answer == 'N':
            INSTALL = False
            break
        else:
            print('')
            dialog('Por favor digite apenas "S" ou "N" !!', color='lr')
            print('')

    if INSTALL:
        os.system('python3 installer.py')
        dialog('INSTALAÇÃO CONCLUÍDA!', color='orange')
        dialog('Tente usar "wihunter" no seu terminal', color='cian')
    else:
        os.system('chmod +x wihunter.py')
        dialog('INSTALAÇÃO CONCLUÍDA!', color='orange')
    os.system('chmod +x uninstall.py')

    # dialog('Baixando Xerosploit...', color='blue')
    # os.system('git clone https://github.com/LionSec/xerosploit')
    # dialog('iniciando instalação...', color='blue')
    # os.system('cp xerosploit-installation-files/xerosploit-installer2-to-3.py xerosploit/install.py')
    # os.system('python xerosploit/install.py')
    # os.system('cp xerosploit-installation-files/xerosploit-python2-to-3.py xerosploit/xerosploit.py')
    # os.system('cp xerosploit-installation-files/xerosploit-python2-to-3.py /opt/xerosploit/xerosploit.py')



main()