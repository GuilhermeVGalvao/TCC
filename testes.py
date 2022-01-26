#!/usr/bin/python3

import os
import re

CURRENT_PATH = os.getcwd()
LOGS_PATH = os.path.join( CURRENT_PATH, 'airodump-logs' )
OUTPUTPATH = os.path.join( LOGS_PATH, 'airodump-logs-output.txt' )

def cleanANSIcodes(text):
    ansi_remover = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    realtext = ansi_remover.sub('', text)
    return realtext

count = -1
index_bssid = 0
real_index_bssid = 0
with open(OUTPUTPATH) as output_file:
    for line in output_file.readlines():
        count += 1
        if 'BSSID' in line:
            real_index_bssid = index_bssid
            index_bssid = count
    print(index_bssid)
    print(real_index_bssid)

with open(OUTPUTPATH) as output_file:
    networks = output_file.readlines()[real_index_bssid:index_bssid]

wpslist = {}
for line in networks:
    line = cleanANSIcodes(line)
    
    real_elements = []
    elements = line.split(' ')
    if 'Quitting' in line:
        continue
    for element in elements:
        if element != '' and element != '\n':
            real_elements.append(element)
    wpslist[ real_elements[0] ] = real_elements[10].replace('Locke\n', 'Locke')
print(wpslist)


'''
    airodump = Popen( ['airodump-ng', interface, '--wps'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
    
    dialog('Iniciar busca por redes? (Aperte Enter)', color='lb')
    input()

    printer = threading.Thread(target=showoutput, args=[airodump])
    printer.start()
    printer.join()


def showoutput(process):
    for line in process.stdout:  # replace '' with b'' for Python 3
        sys.stdout.write(line.decode() )
'''

'''
#!/usr/bin/python3

COLORS = {
    "purple": '\033[95m',
    "blue": '\033[94m',
    "light blue": '\033[96m',
    "cian": '\033[92m',
    "orange": '\033[93m',
    "red": '\033[91m',
    "white": '\033[0m',

    "p": '\033[95m',
    "b": '\033[94m',
    "lb": '\033[96m',
    "c": '\033[92m',
    "o": '\033[93m',
    "r": '\033[91m',
    "w": '\033[0m'
}

STYLE = {
    "default": '',
    "bold": '\033[1m',
    "underscore": '\033[4m'
}

ENDCOLOR = '\033[m'

def dialog(*msg, color='white', style='default', end='\n'):
    if color not in COLORS.keys():
        color = 'white'
    if style not in style:
        style = 'default'
    
    message = ''
    for element in msg:
        message += element + ' '
    message = message.strip()
    final_message = COLORS[color] +'[*]'+ STYLE[style] +' '+ message +' '+ ENDCOLOR

    print(final_message, end=end)

    text = '[*] ' + message
    styled_text = final_message
    return (text, styled_text)

'''