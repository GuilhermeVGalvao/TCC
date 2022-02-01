#!/usr/bin/python3
import sys
import nethunter
import netmanager
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
    '--organize-by-beacons', 
    '-h',
    '--help'
]

args = sys.argv[:]

def main():
    global CAN_EXECUTE

    tester()
    if CAN_EXECUTE:
        start()

### Função que controla todo o programa ###
def start():
    global INTERFACE, AIRODUMP_TIMEOUT, PRINTS_DELAY, CAN_EXECUTE, KEY_TO_NETWORKS_ORGANIZATION, PRINTS_DELAY
    
    has_an_error = nethunter.start( interface=INTERFACE, maxtimeout=AIRODUMP_TIMEOUT, delay=PRINTS_DELAY )
    
    if has_an_error:
        dialog('OCORREU UM ERRO DURANTE A EXECUÇÃO DO AIRODUMP, ABORTANDO EXECUSSÃO!', color='lr')
        dialog('Em caso de dúvida, use o argumento "-h" ou "--help"', color='cian')
        return

    netmanager.start( KEY_TO_NETWORKS_ORGANIZATION )
    wifite_attacker.start()

def tester():
    global INTERFACE, AIRODUMP_TIMEOUT, CAN_EXECUTE, KEY_TO_NETWORKS_ORGANIZATION, PRINTS_DELAY

    if len(args) < 2:
        helper()
        CAN_EXECUTE = False
        return CAN_EXECUTE
    elif len(args) >= 2:
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
                dialog('Em caso de dúvida, use o argumento "-h" ou "--help"', color='cian')
                CAN_EXECUTE = False
                return CAN_EXECUTE
            except IndexError as e:
                dialog('Valor do timeout faltando (números inteiros maiores que 5)', color='lr')
                dialog('Em caso de dúvida, use o argumento "-h" ou "--help"', color='cian')
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
                dialog('Em caso de dúvida, use o argumento "-h" ou "--help"', color='cian')
                CAN_EXECUTE = False
                return CAN_EXECUTE
        elif '-h' in args or '--help' in args:
            helper()
            CAN_EXECUTE = False
            return CAN_EXECUTE
        else:
            dialog(f'    "{args[1:]}" argumento(s) não reconhecido(s)!', color='lr')
            CAN_EXECUTE = False
            return CAN_EXECUTE

def helper(color='blue', symbol_color='blue'):
    w = '\033[0m'
    o = '\033[93m'
    b = '\033[94m'
    e = '\033[m'
    c = '\033[92m'
    r = '\033[91m'
    lr = '\033[31m'

    dialog(f'[MANUAL DO USUÁRIO]', color='blue')
    dialog(f'', color='blue')
    dialog(f'ARGUMENTOS', color='blue')
    dialog(f'----------', color='blue')
    dialog(f'', color='blue')
    dialog(f'{c}-t{b} ou {c}--timeout{b} : Insere de maneira explícita um valor de timeout', color=color)
    dialog(f'                  em segundos para a procura por redes wi-fi com o Airodump', color=color)
    dialog(f'                  <{w}int{c}> É preciso ser um valor inteiro maior que 5', color='cian', symbol_color=symbol_color)
    dialog(f'', color=color)
    dialog(f'                  Ex.: sudo ./main.py {o}-t 20{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                       sudo ./main.py {o}--timeoutt 20{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                                      -------------', color=color)
    dialog(f'                                   A busca por redes wi-fi será abortada', color='white', symbol_color=symbol_color)
    dialog(f'                                   automaticamente após 20 segundos', color='white', symbol_color=symbol_color) 
    dialog(f'', color=color)

    dialog(f"{c}-d{b} ou {c}--delay{b} : Insere um valor de delay entre as saídas ({w}print's{b}) do programa", color=color)
    dialog(f'                Por padrão o valor é 0 para o máximo de velocidade, mas é possível', color=color)
    dialog(f'                inserir um valor para tornar a saída mais legível', color=color)
    dialog(f'                <{w}float{c}> É preciso ser um valor de ponto flutuante maior ou igual a 0', color='cian', symbol_color=symbol_color)
    dialog(f'                É recomendado um valor entre zero e no máximo 2', color='cian', symbol_color=symbol_color)
    dialog(f'', color=color)
    dialog(f'                Ex.: sudo ./main.py {o}-d 0.2{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                     sudo ./main.py {o}--delay 0.2{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                                    -----------', color=color)
    dialog(f'                                 Cada saída terá um delay 0.2 segundos em relação à', color='white', symbol_color=symbol_color)
    dialog(f'                                 saída anterior', color='white', symbol_color=symbol_color) 
    dialog(f'', color=color)

    dialog(f'{c}-m{b} ou {c}--manual-control{b} : A busca por redes wi-fi com o Airodump deixará de ter', color=color)
    dialog(f'                         valor de timeout e será controlada manualmente, parando', color=color)
    dialog(f'                         apenas quando o usuário apertar CTRL + C', color=color)
    dialog(f'', color=color)
    dialog(f'                  Ex.: sudo ./main.py {o}-m{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                       sudo ./main.py {o}--manual-control{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                                      -------------', color=color)
    dialog(f'                                   A busca por redes wi-fi é infinita e só', color='white', symbol_color=symbol_color)
    dialog(f'                                   parará quando o usuário apertar CTRL + C', color='white', symbol_color=symbol_color) 
    dialog(f'', color=color)

    dialog(f'{c}--organize-by-power{b} : Ordena ao programa que organize as redes a seres atacadas', color=color)
    dialog(f'                      por ordem de "power" (ou potência do sinal)', color=color)
    dialog(f'                      O driver de algumas interfaces de rede pode não ser compatível', color=color)
    dialog(f'                      com essa opção ou apresentar mal funcionamento, nesse caso,', color=color)
    dialog(f'                      recomenda-se o uso do argumento "--organize-by-beacons"', color=color)
    dialog(f'', color=color)
    dialog(f'                  Ex.: sudo ./main.py {o}--organize-by-power{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                                      -------------------', color=color)
    dialog(f'                                   O programa dará preferência a programas com maior', color='white', symbol_color=symbol_color)
    dialog(f'                                   "power" (ou potência do sinal) no momento de atacar', color='white', symbol_color=symbol_color) 
    dialog(f'', color=color)

    dialog(f'{c}--organize-by-beacons{b} : Ordena ao programa que organize as redes a seres atacadas', color=color)
    dialog(f'                        por ordem de "beacons encontrados"', color=color)
    dialog(f'                        Essa é a opção padrão devido ao driver de algumas interfaces de rede', color=color)
    dialog(f'                        não serem compatíveis ou apresentarem mal funcionamento com a', color=color)
    dialog(f'                        opção "--organize-by-power", mas se você não encontrar problemas', color=color)
    dialog(f'                        com a outra opção, recomenda-se usá-la', color=color)
    dialog(f'', color=color)
    dialog(f'                  Ex.: sudo ./main.py {o}--organize-by-beacons{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                                      -------------------', color=color)
    dialog(f'                                   O programa dará preferência a programas com maior', color='white', symbol_color=symbol_color)
    dialog(f'                                   número de beacons capturados no momento de atacar', color='white', symbol_color=symbol_color) 
    dialog(f'', color=color)

    dialog(f'{c}-h{b} ou {c}--help{b} : Exibe o manual de ajuda do usuário', color=color)
    dialog(f'', color=color)
    dialog(f'                  Ex.: sudo ./main.py {o}-h{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                       sudo ./main.py {o}--help{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                                      ------', color=color)
    dialog(f'                                   A busca por redes wi-fi será abortada', color='white', symbol_color=symbol_color)
    dialog(f'                                   automaticamente após 20 segundos', color='white', symbol_color=symbol_color) 
    dialog(f'', color=color)


if __name__ == '__main__':
    main()