#!/usr/bin/python3

import os
import sys
from printer import dialog

CURRENT_PATH = os.getcwd()

def main():
    global CURRENT_PATH

    lr = '\033[31m'

    if not os.getuid() == 0:
        sys.exit(f'{lr}[*] O instalador deve ser executado como superusuário!')
    
    dialog('Atualizando repositórios do sistema...', color='blue')
    os.system('apt-get update -y')

    dialog('Instalando git...', color='blue')
    os.system('apt-get install -y git')

    dialog('Instalando aircrack-ng...', color='blue')
    os.system('apt-get install -y aircrack-ng')

    dialog('Instalando Wifite...', color='blue')
    os.system('apt-get install -y wifite')

    dialog('Baixando Xerosploit...', color='blue')
    os.system('git clone https://github.com/LionSec/xerosploit')
    dialog('iniciando instalação...', color='blue')
    os.system('cp xerosploit-installation-files/xerosploit-installer2-to-3.py xerosploit/install.py')
    os.system('python xerosploit/install.py')
    os.system('cp xerosploit-installation-files/xerosploit-python2-to-3.py xerosploit/xerosploit.py')
    os.system('cp xerosploit-installation-files/xerosploit-python2-to-3.py /opt/xerosploit/xerosploit.py')



main()