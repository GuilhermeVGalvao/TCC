#!/usr/bin/python3

import os

def main():
    # Delete program directory and files
    os.system( 'rm -rf /opt/wihunter/' )

    # Del the .sh executable in /usr/bin
    os.system('rm -f /usr/bin/wihunter')


if __name__ == '__main__':
    main()