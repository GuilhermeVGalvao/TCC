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
