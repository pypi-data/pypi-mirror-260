import os
    
def getBasePath():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def getWinUser():
    os.getlogin()

def comparaStr(bot, valorRef):
    i = 0
    while i < 3:
        bot.control_a()
        bot.control_c()
        bot.type_keys(valorRef)
        bot.control_a()
        bot.control_c()
        if valorRef != bot.get_clipboard():
            bot.control_a()
            bot.control_c()
        else:
            break
        i += 1
    if i >= 3:
        raise Exception(f'erro ao digitar - palavra a ser escrita: {valorRef}')
