#!/usr/bin/python3

import os
import sys
from  Wihunter import nethunter
from  Wihunter import netmanager
from  Wihunter import wifite_attacker
from  printer import dialog

################################################################################
###                                                                          ###
###           WIHUNTER HAS BEEN CREATED BY GUILHERME VIEIRA GALVÃO           ###
###                   GITHUB: github.com/GuilhermeVGalvao/                   ###
###                                                                          ###
###                             GuilhermeVGalvao                             ###
###                          Instagram: @galvao.exe                          ###
###                           Twitter: @galvao_exe                           ###
###                                                                          ###
###--------------------------------------------------------------------------###
###                                                                          ###
### Wihunter is a free software: You can use, redistribute and/or modify     ###
###                                                                          ###
### Whihunter uses Aircrack and Wifite Tecnologies, you can find them in:    ###
### https://www.aircrack-ng.org/ and                                         ###
### https://github.com/kimocoder/wifite2                                     ###
###                                                                          ###
###--------------------------------------------------------------------------###
###                                                                          ###
###              "With great power comes greate responsibility"              ###
###                                                                          ###
################################################################################

### Variáveis Globais ###
INTERFACE = ''
AIRODUMP_TIMEOUT = 10
CAN_EXECUTE = True
KEY_TO_NETWORKS_ORGANIZATION = 'beacons'
PRINTS_DELAY = 0
KILL_ANOTHER_PROCESSES = None

ARGS_LIST = [
    '-d',
    '--delay',
    '--kill',
    '-m',
    '--manual-control',
    '--organize-by-beacons', 
    '--organize-by-power',
    '-t', 
    '--timeout',
    '--uninstall',
    '-w',
    '--word-list',
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
    global INTERFACE, AIRODUMP_TIMEOUT, PRINTS_DELAY, CAN_EXECUTE, KEY_TO_NETWORKS_ORGANIZATION, PRINTS_DELAY, KILL_ANOTHER_PROCESSES
    
    has_an_error = nethunter.start( interface=INTERFACE, maxtimeout=AIRODUMP_TIMEOUT, delay=PRINTS_DELAY )
    
    if has_an_error:
        dialog('OCORREU UM ERRO DURANTE A EXECUÇÃO DO AIRODUMP, ABORTANDO EXECUSSÃO!', color='lr')
        dialog('Em caso de dúvida, use o argumento "-h" ou "--help"', color='cian')
        return

    netmanager.start( KEY_TO_NETWORKS_ORGANIZATION )
    wifite_attacker.start( kill=KILL_ANOTHER_PROCESSES )


def tester():
    global INTERFACE, AIRODUMP_TIMEOUT, CAN_EXECUTE, KEY_TO_NETWORKS_ORGANIZATION, PRINTS_DELAY, KILL_ANOTHER_PROCESSES

    w = '\033[0m'
    o = '\033[93m'
    b = '\033[94m'
    e = '\033[m'
    c = '\033[92m'
    r = '\033[91m'
    lr = '\033[31m'

    if len(args) < 2:
        helper()
        CAN_EXECUTE = False
        return CAN_EXECUTE

    while True:
        if len( args ) <= 1:
            if INTERFACE == '' or INTERFACE is None:
                CAN_EXECUTE = False
                dialog('INTERFACE DE REDE NÃO ESPECIFICADA!', color='lr')
            break

        # Casos desfavoráveis
        if '-t' in args and '--timeout' in args:
            CAN_EXECUTE = False
            return CAN_EXECUTE
        
        if '-m' in args and '--manual-control' in args:
            CAN_EXECUTE = False
            return CAN_EXECUTE

        if '-m' in args and '-t' in args:
            CAN_EXECUTE = False
            return CAN_EXECUTE

        if '--timeout' in args and '--manual-control' in args:
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
                dialog('Valor do timeout faltando (números inteiros maiores que 5)'.upper(), color='lr')
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
        elif '--kill' in args:
            i = args.index('--kill')
            KILL_ANOTHER_PROCESSES = True
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
            except IndexError as e:
                dialog('VALOR DE DELAY NÃO ESPECIFICADO!', color='lr')
                dialog('Digite apenas valores de delay válidos (números reais positivos)', color='lr')
                dialog('Em caso de dúvida, use o argumento "-h" ou "--help"', color='cian')
                CAN_EXECUTE = False
                return CAN_EXECUTE
        elif '--uninstall' in args:
            if os.path.exists('/opt/wihunter/uninstall.py'):
                dialog('Deseja realmente desinstalar o Wihunter? (S/N)', color='lr')
                answer = input('>> ').upper()

                if answer == 'S':
                    os.system('python3 /opt/wihunter/uninstall.py')
                    os.exit('')
                elif answer == 'N':
                    dialog('Desinstalação cancelada!', color='white')
                    os.exit('')
                else:
                    dialog('Por favor digite apenas "S" ou "N"', color='white')
                    os.exit('')
            else:
                dialog('Wihunter não está instalado no sistema')
                dialog('para ser desinstalado')
                os.exit('')
        elif '-h' in args or '--help' in args:
            helper()
            CAN_EXECUTE = False
            return CAN_EXECUTE
        elif '-' in args[-1]:
            dialog(f'    "{args[1:]}" argumento(s) não reconhecido(s)!', color='lr', style='bold')
            CAN_EXECUTE = False
            return CAN_EXECUTE
        elif len(args) == 2:
            INTERFACE = args.pop()
            continue
        else:
            dialog(f'    "{o}{args[1:]}{lr}" argumento(s) não reconhecido(s)!', color='lr')
            CAN_EXECUTE = False
            return CAN_EXECUTE


w = '\033[0m'
o = '\033[93m'
b = '\033[94m'
e = '\033[m'
c = '\033[92m'
r = '\033[91m'
lr = '\033[31m'

def helper(color='blue', symbol_color='blue'):

    dialog(f'[MANUAL DO USUÁRIO]', color='blue')
    dialog(f'', color='blue')
    dialog(f'ARGUMENTOS', color='blue')
    dialog(f'----------', color='blue')
    dialog(f'', color='blue')

    show_delay_help( color=color, symbol_color=symbol_color )
    show_kill_help( color=color, symbol_color=symbol_color )
    show_manual_control_help( color=color, symbol_color=symbol_color )
    show_organize_by_beacons_help( color=color, symbol_color=symbol_color )
    show_organize_by_power_help( color=color, symbol_color=symbol_color )
    show_timeout_help( color=color, symbol_color=symbol_color )
    show_wordlist_help( color=color, symbol_color=symbol_color )
    show_help( color=color, symbol_color=symbol_color )


def show_delay_help(color='white', symbol_color='white'):
    dialog(f"{c}-d{b} ou {c}--delay{b} : Insere um valor de delay entre as saídas ({w}print's{b})", color=color)
    dialog(f"                do programa", color=color)
    dialog(f'', color=color)
    dialog(f'                Por padrão o valor é 0 para o máximo de velocidade,', color=color)
    dialog(f'                mas é possível inserir um valor para tornar a saída', color=color)
    dialog(f'                mais legível', color=color)
    dialog(f'                <{w}float{c}> É preciso ser um valor de ponto flutuante', color='cian', symbol_color=symbol_color)
    dialog(f'                maior ou igual a 0', color='cian', symbol_color=symbol_color)
    dialog(f'                É recomendado um valor entre zero e no máximo 2', color='cian', symbol_color=symbol_color)
    dialog(f'', color=color)
    dialog(f'                Ex.: sudo wihunter {o}-d 0.2{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                     sudo wihunter {o}--delay 0.2{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                                   -----------', color=color)
    dialog(f'                                 Cada saída terá um delay 0.2', color='white', symbol_color=symbol_color)
    dialog(f'                                 segundos em relação à saída', color='white', symbol_color=symbol_color)
    dialog(f'                                 anterior', color='white', symbol_color=symbol_color) 
    dialog(f'', color=color)


def show_kill_help(color='white', symbol_color='white'):
    dialog(f'{c}--kill{b} : Mata processos em conflito com o Wifite', color=color)
    dialog(f'', color=color)
    dialog(f'         Durante o ataque às redes Wi-fi, alguns', color=color)
    dialog(f'         processos podem entrar em conflito com o', color=color)
    dialog(f'         Wifite e causar instabilidades; caso isso ocorra,', color=color)
    dialog(f'         use essa opção para matar todos os processos que', color=color)
    dialog(f'         possam estar causando conflito', color=color)
    dialog(f'', color=color)
    dialog(f'                  Ex.: sudo wihunter {o}--kill{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                                     ------', color=color)
    dialog(f'                                   O programa matará todos os', color='white', symbol_color=symbol_color)
    dialog(f'                                   processos que possam entrar', color='white', symbol_color=symbol_color)
    dialog(f'                                   em conflito com o Wifite', color='white', symbol_color=symbol_color)
    dialog(f'                                   durante a sequência de ataques', color='white', symbol_color=symbol_color)
    dialog(f'', color=color)


def show_manual_control_help(color='white', symbol_color='white'):
    dialog(f'{c}-m{b} ou {c}--manual-control{b} : A busca por redes wi-fi com o Airodump', color=color)
    dialog(f'                         deixará de ter valor de timeout e será', color=color)
    dialog(f'                         controlada manualmente, parando apenas', color=color)
    dialog(f'                         quando o usuário apertar CTRL + C', color=color)
    dialog(f'', color=color)
    dialog(f'                  Ex.: sudo wihunter {o}-m{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                       sudo wihunter {o}--manual-control{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                                     ----------------', color=color)
    dialog(f'                                   A busca por redes wi-fi é infinita', color='white', symbol_color=symbol_color)
    dialog(f'                                   e só parará quando o usuário apertar', color='white', symbol_color=symbol_color) 
    dialog(f'                                   CTRL + C', color='white', symbol_color=symbol_color) 
    dialog(f'', color=color)


def show_organize_by_beacons_help(color='white', symbol_color='white'):
    dialog(f'{c}--organize-by-beacons{b} : Ordena ao programa que organize as redes', color=color)
    dialog(f'                        a serem atacadas por ordem de "beacons', color=color)
    dialog(f'                        encontrados"', color=color)
    dialog(f'', color=color)
    dialog(f'                        Essa é a opção padrão devido ao driver de', color=color)
    dialog(f'                        algumas interfaces de rede não serem', color=color)
    dialog(f'                        compatíveis ou apresentarem mal funcionamento', color=color)
    dialog(f'                        com a opção "--organize-by-power", mas se', color=color)
    dialog(f'                        você não encontrar problemas com a outra,', color=color)
    dialog(f'                        opção recomenda-se usá-la', color=color)
    dialog(f'', color=color)
    dialog(f'                  Ex.: sudo wihunter {o}--organize-by-beacons{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                                     ---------------------', color=color)
    dialog(f'                                   O programa dará preferência a', color='white', symbol_color=symbol_color)
    dialog(f'                                   programas com maior número de', color='white', symbol_color=symbol_color)
    dialog(f'                                   beacons capturados no momento', color='white', symbol_color=symbol_color) 
    dialog(f'                                   de atacar', color='white', symbol_color=symbol_color) 
    dialog(f'', color=color)


def show_organize_by_power_help(color='white', symbol_color='white'):
    dialog(f'{c}--organize-by-power{b} : Ordena ao programa que organize as redes', color=color)
    dialog(f'                      a serem atacadas por ordem de "power"', color=color)
    dialog(f'                      (ou potência do sinal)', color=color)
    dialog(f'', color=color)
    dialog(f'                      O driver de algumas interfaces de rede', color=color)
    dialog(f'                      pode não ser compatível com essa opção', color=color)
    dialog(f'                      ou apresentar mal funcionamento, nesse caso,', color=color)
    dialog(f'                      recomenda-se o uso do argumento', color=color)
    dialog(f'                      "--organize-by-beacons"', color=color)
    dialog(f'', color=color)
    dialog(f'                  Ex.: sudo wihunter {o}--organize-by-power{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                                     -------------------', color=color)
    dialog(f'                                   O programa dará preferência a', color='white', symbol_color=symbol_color)
    dialog(f'                                   programas com maior "power"', color='white', symbol_color=symbol_color)
    dialog(f'                                   (ou potência do sinal) no', color='white', symbol_color=symbol_color) 
    dialog(f'                                   momento de atacar', color='white', symbol_color=symbol_color) 
    dialog(f'', color=color)


def show_timeout_help(color='white', symbol_color='white'):
    dialog(f'{c}-t{b} ou {c}--timeout{b} : Insere de maneira explícita um valor de timeout', color=color)
    dialog(f'                  em segundos para a procura por redes wi-fi com', color=color)
    dialog(f'                  o Airodump', color=color)
    dialog(f'                  <{w}int{c}> É preciso ser um valor inteiro maior que 5', color='cian', symbol_color=symbol_color)
    dialog(f'', color=color)
    dialog(f'                  Ex.: sudo wihunter {o}-t 20{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                       sudo wihunter {o}--timeoutt 20{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                                     -------------', color=color)
    dialog(f'                                   A busca por redes wi-fi será abortada', color='white', symbol_color=symbol_color)
    dialog(f'                                   automaticamente após 20 segundos', color='white', symbol_color=symbol_color) 
    dialog(f'', color=color)


def show_wordlist_help(color='white', symbol_color='white'):
    dialog(f'{c}-w{b} ou {c}--wordlist{b} : Indica a wordlist que deve ser usada para a', color=color)
    dialog(f'                   quebra de senhas em ataques a redes WPA/WPA2', color=color)
    dialog(f'', color=color)
    dialog(f'                   Caso não seja indicada, será usada a wordlist', color=color)
    dialog(f'                   padrão do Wifite, a wordlist-probable.txt', color=color)
    dialog(f'                   <{w}File Path{c}> É preciso ser um arquivo', color='cian', symbol_color=symbol_color)
    dialog(f'                   (ou o caminho para um arquivo) de wordlist', color='cian', symbol_color=symbol_color)
    dialog(f'                   e com as devidas formatações', color='cian', symbol_color=symbol_color)
    dialog(f'', color=color)
    dialog(f'                  Ex.: sudo wihunter {o}-w /home/user/Documents/pass.txt{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                       sudo wihunter {o}--wordlist my-wordlist.txt20{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                                     ----------------------------', color=color)
    dialog(f'                                   A busca por redes wi-fi será abortada', color='white', symbol_color=symbol_color)
    dialog(f'                                   automaticamente após 20 segundos', color='white', symbol_color=symbol_color) 
    dialog(f'', color=color)


def show_help(color='white', symbol_color='white'):
    dialog(f'{c}-h{b} ou {c}--help{b} : Exibe o manual de ajuda do usuário', color=color)
    dialog(f'', color=color)
    dialog(f'                  Ex.: sudo wihunter {o}-h{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                       sudo wihunter {o}--help{b} wlan0', color=color, symbol_color=symbol_color)
    dialog(f'                                     ------', color=color)
    dialog(f'                                   Abre esse menu em que você', color='white', symbol_color=symbol_color)
    dialog(f'                                   está agora :)', color='white', symbol_color=symbol_color) 
    dialog(f'', color=color)


if __name__ == '__main__':
    main()