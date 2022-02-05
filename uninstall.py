#!/usr/bin/python3

import os
import sys
from time import sleep

lr = '\033[31m'

def main():
    if not os.getuid() == 0:
        sys.exit(f'{lr}[*] O desinstalador deve ser executado como superusuário!')

    # Delete program directory and files
    print('[*] Removendo arquivos e diretórios...')
    sleep(0.2)
    os.system( 'rm -rf /opt/wihunter/' )

    # Del the .sh executable in /usr/bin
    print('[*] Excluíndo wihunter...')
    sleep(0.2)
    os.system('rm -f /usr/bin/wihunter')


if __name__ == '__main__':
    main()