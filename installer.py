#!/usr/bin/python3

import os
import sys
from printer import dialog

CURRENT_PATH = os.getcwd()

def main():
    global CURRENT_PATH

    if not os.getuid() == 0:
        sys.exit('O instalador deve ser executado como superusuário!')
    
    dialog('Atualizando repositórios do sistema...', color='blue')
    os.system('apt-get update -y')

    dialog('Instalando git...', color='blue')
    os.system('apt-get install -y git')

    dialog('Instalando aircrack-ng...', color='blue')
    os.system('apt-get install -y aircrack-ng')

    dialog('Instalando Wifite...', color='blue')
    os.system('apt-get install -y wifite')

    # dialog('Baixando Xerosploit...', color='blue')
    # os.system('git clone https://github.com/LionSec/xerosploit')
    # os.system('python2 xerosploit/install.py')


main()