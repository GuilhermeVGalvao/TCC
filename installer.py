#!/usr/bin/python3

import os

def main():
    # Make program directory
    os.makedirs( '/opt/wihunter' )

    # Copy files to Wihunter's directory
    os.system('cp wihunter.py /opt/wihunter/')
    os.system('cp printer.py /opt/wihunter/')
    os.system('cp -r Wihunter /opt/wihunter/')
    os.system('cp uninstall.py /opt/wihunter/')

    # Copy the .sh executable to /usr/bin
    os.system('cp wihunter.sh /usr/bin/wihunter')

    # Set execute permission in wihunter
    os.system('chmod +x /usr/bin/wihunter')


if __name__ == '__main__':
    main()