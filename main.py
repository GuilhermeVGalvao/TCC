#!/usr/bin/python3
import sys
import nethunter
import netmanager
import netinvader
import wifite_attacker

### Variáveis Globais ###
interface = ''
airodump_timeout = 10
can_execute = False

args = sys.argv[:]

for i in range( len(args) ):
    if args[i] == '-t':
        try:
            airodump_timeout = int(args.pop(i+1))
            args.pop(i)
        except ValueError as e:
            print('Digite apenas valores de timeout válidos (números inteiros)')
        break

if len(args) >= 2:
    interface = args.pop()
    can_execute = True
else:
    print('Interface de rede não foi expecificada')
    can_execute = False


if can_execute:
    nethunter.start( interface=interface, maxtimeout=airodump_timeout )
    #netmanager.start()
    #wifite_attacker.start()
    