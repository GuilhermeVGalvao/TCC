#!/usr/bin/python3

import os
import sys

lr = '\033[31m'

def main():
    if not os.getuid() == 0:
        sys.exit(f'{lr}[*] O desinstalador deve ser executado como superusuário!')

    # Delete program directory and files
    os.system( 'rm -rf /opt/wihunter/' )

    # Del the .sh executable in /usr/bin
    os.system('rm -f /usr/bin/wihunter')


if __name__ == '__main__':
    main()