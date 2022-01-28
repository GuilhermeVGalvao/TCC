#!/usr/bin/python3
import sys
import nethunter
import netmanager
import netinvader
import wifite_attacker
from printer import dialog

### Variáveis Globais ###
INTERFACE = ''
AIRODUMP_TIMEOUT = 10
CAN_EXECUTE = True
KEY_TO_NETWORKS_ORGANIZATION = 'beacons'
PRINTS_DELAY = 0

ARGS_LIST = [
    '-t', 
    '--timeout',
    '-d',
    '--delay',
    '-m',
    '--manual-control',
    '--organize-by-power',
    '--organize-by-beacons'
]

args = sys.argv[:]

### Função principal ###
def start():
    global INTERFACE, AIRODUMP_TIMEOUT, PRINTS_DELAY
    
    has_an_error = nethunter.start( interface=INTERFACE, maxtimeout=AIRODUMP_TIMEOUT, delay=PRINTS_DELAY )
    
    if has_an_error:
        dialog('OCORREU UM ERRO DURANTE A EXECUÇÃO DO AIRODUMP, ABORTANDO EXECUSSÃO!', color='lr')
        return

    netmanager.start( KEY_TO_NETWORKS_ORGANIZATION )
    wifite_attacker.start()

def tester():
    global INTERFACE, AIRODUMP_TIMEOUT, CAN_EXECUTE, KEY_TO_NETWORKS_ORGANIZATION, PRINTS_DELAY

    if len(args) >= 2:
        INTERFACE = args.pop()
    else:
        print('INTERFACE de rede não foi expecificada')
        CAN_EXECUTE = False
        return CAN_EXECUTE

    while True:
        if len( args ) <= 1:
            break

        # Casos desfavoráveis
        if '-t' in args and '--timeout' in args:
            CAN_EXECUTE = False
            return CAN_EXECUTE
        
        if '-m' in args and '--manual-control' in args:
            CAN_EXECUTE = False
            return CAN_EXECUTE
        
        if '-d' in args and '--delay' in args:
            CAN_EXECUTE = False
            return CAN_EXECUTE

        # Casos favoráveis
        if '-t' in args or '--timeout' in args:
            if '-t' in args:
                i = args.index('-t')
            else:
                i = args.index('--timeout')
            try:
                if int( args[i+1] ) <= 5:
                    raise ValueError
                AIRODUMP_TIMEOUT = int(args.pop(i+1))
                args.pop(i)
                continue
            except ValueError as e:
                dialog('Digite apenas valores de timeout válidos (números inteiros maiores que 5)', color='lr')
                CAN_EXECUTE = False
                return CAN_EXECUTE
            except IndexError as e:
                dialog('Valor do timeout faltando (números inteiros maiores que 5)', color='lr')
                CAN_EXECUTE = False
                return CAN_EXECUTE
        elif '-m' in args or '--manual-control' in args:
            if '-m' in args:
                i = args.index('-m')
            else:
                i = args.index('--manual-control')
            AIRODUMP_TIMEOUT = None
            args.pop(i)
            continue
        elif '--organize-by-power' in args:
            i = args.index('--organize-by-power')
            KEY_TO_NETWORKS_ORGANIZATION = 'power'
            args.pop(i)
            continue
        elif '--organize-by-beacons' in args:
            i = args.index('--organize-by-beacons')
            KEY_TO_NETWORKS_ORGANIZATION = 'beacons'
            args.pop(i)
            continue
        elif '-d' in args or '--delay' in args:
            if '-d' in args:
                i = args.index('-d')
            else:
                i = args.index('--delay')
            try:
                if float( args[i+1] ) >= 0:
                    PRINTS_DELAY = float(args.pop(i+1))
                    args.pop(i)
                    continue
                else:
                    raise ValueError
            except ValueError as e:
                dialog('Digite apenas valores de delay válidos (números reais positivos)', color='lr')
                CAN_EXECUTE = False
                return CAN_EXECUTE
        else:
            dialog(f'    "{args[1:]}" argumento(s) não reconhecido(s)!', color='lr')
            CAN_EXECUTE = False
            return CAN_EXECUTE

tester()
if CAN_EXECUTE:
    start()
    