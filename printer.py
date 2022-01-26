#!/usr/bin/python3

COLORS = {
    "purple": '\033[95m',
    "blue": '\033[94m',
    "light blue": '\033[96m',
    "cian": '\033[92m',
    "orange": '\033[93m',
    "red": '\033[91m',
    "light red": '\033[31m',
    "white": '\033[0m',

    "p": '\033[95m',
    "b": '\033[94m',
    "lb": '\033[96m',
    "c": '\033[92m',
    "o": '\033[93m',
    "r": '\033[91m',
    "lr": '\033[31m',
    "w": '\033[0m'
}

STYLE = {
    "default": '',
    "bold": '\033[1m',
    "underscore": '\033[4m'
}

ENDCOLOR = '\033[m'

def dialog(*msg, color='white', style='default', symbol='[*]', symbol_color=None, end='\n'):
    if color not in COLORS.keys():
        color = 'white'
    if style not in style:
        style = 'default'
    if symbol_color not in COLORS.keys() or symbol_color == None:
        symbol_color = color
    if symbol == None:
        symbol = ''

    message = ''
    for element in msg:
        message += ' ' + element
    message = message[1:]

    symbol_text = COLORS[symbol_color] +symbol+ ENDCOLOR
    message = COLORS[color] + STYLE[style] +' '+message+' '+ ENDCOLOR

    final_message = symbol_text + message


    print(final_message, end=end)

    if symbol == '':
        text = message
    else:
        text = symbol +' '+ message

    styled_text = final_message
    return (text, styled_text)


def show_wep_menu(color='c', style='bold'):
    dialog('=== INICIANDO ATAQUE ÀS REDES WEP ===', color=color, style=style)
    dialog('      ___           ___           ___   ', symbol='    ', color=color, style=style)
    dialog('     /__/\         /  /\         /  /\  ', symbol='    ', color=color, style=style)
    dialog('    _\_ \:\       /  /:/_       /  /::\ ', symbol='    ', color=color, style=style)
    dialog('   /__/\ \:\     /  /:/ /\     /  /:/\:\ ', symbol='    ', color=color, style=style)
    dialog('  _\_ \:\ \:\   /  /:/ /:/_   /  /:/~/:/', symbol='    ', color=color, style=style)
    dialog(' /__/\ \:\ \:\ /__/:/ /:/ /\ /__/:/ /:/ ', symbol='    ', color=color, style=style)
    dialog(' \  \:\ \:\/:/ \  \:\/:/ /:/ \  \:\/:/  ', symbol='    ', color=color, style=style)
    dialog('  \  \:\ \::/   \  \::/ /:/   \  \::/   ', symbol='    ', color=color, style=style)
    dialog('   \  \:\/:/     \  \:\/:/     \  \:\   ', symbol='    ', color=color, style=style)
    dialog('    \  \::/       \  \::/       \  \:\  ', symbol='    ', color=color, style=style)
    dialog('     \__\/         \__\/         \__\/  ', symbol='    ', color=color, style=style)

    '''
    / )( \(  __)(  _ \
    \ /\ / ) _)  ) __/ 
    (_/\_)(____)(__)   

          ___           ___           ___   
         /__/\         /  /\         /  /\  
        _\_ \:\       /  /:/_       /  /::\ 
       /__/\ \:\     /  /:/ /\     /  /:/\:\
      _\_ \:\ \:\   /  /:/ /:/_   /  /:/~/:/
     /__/\ \:\ \:\ /__/:/ /:/ /\ /__/:/ /:/ 
     \  \:\ \:\/:/ \  \:\/:/ /:/ \  \:\/:/  
      \  \:\ \::/   \  \::/ /:/   \  \::/   
       \  \:\/:/     \  \:\/:/     \  \:\   
        \  \::/       \  \::/       \  \:\  
         \__\/         \__\/         \__\/    
    '''


def show_wpa_menu(color='o', style='bold'):
    dialog('=== INICIANDO ATAQUE ÀS REDES WPA ===', color=color, style=style)
    dialog('      ___           ___         ___      ', symbol='    ', color=color, style=style)
    dialog('     /__/\         /  /\       /  /\     ', symbol='    ', color=color, style=style)
    dialog('    _\_ \:\       /  /::\     /  /::\    ', symbol='    ', color=color, style=style)
    dialog('   /__/\ \:\     /  /:/\:\   /  /:/\:\   ', symbol='    ', color=color, style=style)
    dialog('  _\_ \:\ \:\   /  /:/~/:/  /  /:/~/::\  ', symbol='    ', color=color, style=style)
    dialog(' /__/\ \:\ \:\ /__/:/ /:/  /__/:/ /:/\:\ ', symbol='    ', color=color, style=style)
    dialog(' \  \:\ \:\/:/ \  \:\/:/   \  \:\/:/__\/ ', symbol='    ', color=color, style=style)
    dialog('  \  \:\ \::/   \  \::/     \  \::/      ', symbol='    ', color=color, style=style)
    dialog('   \  \:\/:/     \  \:\      \  \:\      ', symbol='    ', color=color, style=style)
    dialog('    \  \::/       \  \:\      \  \:\     ', symbol='    ', color=color, style=style)
    dialog('     \__\/         \__\/       \__\/     ', symbol='    ', color=color, style=style)


def show_wpa_wps_menu(color='b', style='bold'):
    dialog('=== INICIANDO ATAQUE ÀS REDES WPA COM WPS ===', color=color, style=style)
    dialog('      ___           ___         ___                ___           ___         ___     ', symbol='    ', color=color, style=style)
    dialog('     /__/\         /  /\       /  /\              /__/\         /  /\       /  /\    ', symbol='    ', color=color, style=style)
    dialog('    _\_ \:\       /  /::\     /  /::\            _\_ \:\       /  /::\     /  /:/_   ', symbol='    ', color=color, style=style)
    dialog('   /__/\ \:\     /  /:/\:\   /  /:/\:\          /__/\ \:\     /  /:/\:\   /  /:/ /\  ', symbol='    ', color=color, style=style)
    dialog('  _\_ \:\ \:\   /  /:/~/:/  /  /:/~/::\        _\_ \:\ \:\   /  /:/~/:/  /  /:/ /::\ ', symbol='    ', color=color, style=style)
    dialog(' /__/\ \:\ \:\ /__/:/ /:/  /__/:/ /:/\:\      /__/\ \:\ \:\ /__/:/ /:/  /__/:/ /:/\:\ ', symbol='    ', color=color, style=style)
    dialog(' \  \:\ \:\/:/ \  \:\/:/   \  \:\/:/__\/      \  \:\ \:\/:/ \  \:\/:/   \  \:\/:/~/:/', symbol='    ', color=color, style=style)
    dialog('  \  \:\ \::/   \  \::/     \  \::/            \  \:\ \::/   \  \::/     \  \::/ /:/ ', symbol='    ', color=color, style=style)
    dialog('   \  \:\/:/     \  \:\      \  \:\             \  \:\/:/     \  \:\      \__\/ /:/  ', symbol='    ', color=color, style=style)
    dialog('    \  \::/       \  \:\      \  \:\             \  \::/       \  \:\       /__/:/   ', symbol='    ', color=color, style=style)
    dialog('     \__\/         \__\/       \__\/              \__\/         \__\/       \__\/    ', symbol='    ', color=color, style=style)
    
    '''
          ___           ___         ___     
         /__/\         /  /\       /  /\    
        _\_ \:\       /  /::\     /  /::\   
       /__/\ \:\     /  /:/\:\   /  /:/\:\  
      _\_ \:\ \:\   /  /:/~/:/  /  /:/~/::\ 
     /__/\ \:\ \:\ /__/:/ /:/  /__/:/ /:/\:\
     \  \:\ \:\/:/ \  \:\/:/   \  \:\/:/__\/
      \  \:\ \::/   \  \::/     \  \::/     
       \  \:\/:/     \  \:\      \  \:\     
        \  \::/       \  \:\      \  \:\    
         \__\/         \__\/       \__\/    
    

          ___           ___         ___     
         /__/\         /  /\       /  /\    
        _\_ \:\       /  /::\     /  /:/_   
       /__/\ \:\     /  /:/\:\   /  /:/ /\  
      _\_ \:\ \:\   /  /:/~/:/  /  /:/ /::\ 
     /__/\ \:\ \:\ /__/:/ /:/  /__/:/ /:/\:\
     \  \:\ \:\/:/ \  \:\/:/   \  \:\/:/~/:/
      \  \:\ \::/   \  \::/     \  \::/ /:/ 
       \  \:\/:/     \  \:\      \__\/ /:/  
        \  \::/       \  \:\       /__/:/   
         \__\/         \__\/       \__\/    

    '''