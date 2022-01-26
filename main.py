#!/usr/bin/python3
import sys
import nethunter
import netmanager
import netinvader
import wifite_attacker
from printer import dialog

### Variáveis Globais ###
interface = ''
airodump_timeout = 10
can_execute = False
key_to_networks_organization = 'beacons'

args = sys.argv[:]

### Função principal ###
def start():
    global interface, airodump_timeout
    
    has_an_error = nethunter.start( interface=interface, maxtimeout=airodump_timeout )
    
    if has_an_error:
        dialog('OCORREU UM ERRO DURANTE A EXECUÇÃO DO AIRODUMP, ABORTANDO EXECUSSÃO!', color='lr')
        return

    #netmanager.start( key_to_networks_organization )
    wifite_attacker.start()


for i in range( len(args) ):
    if args[i] == '-t':
        try:
            airodump_timeout = int(args.pop(i+1))
            args.pop(i)
        except ValueError as e:
            print('Digite apenas valores de timeout válidos (números inteiros)')
        break
    elif args[i] == '--organize-by-power':
        key_to_networks_organization = 'power'
    elif args[i] == '--organize-by-beacons':
        key_to_networks_organization = 'beacons'

if len(args) >= 2:
    interface = args.pop()
    can_execute = True
else:
    print('Interface de rede não foi expecificada')
    can_execute = False


if can_execute:
    start()
    