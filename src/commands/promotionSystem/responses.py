import sys
import json
import time

def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == 'rankdata':
        with open('rankData.json', 'r') as infile:
            return str(json.load(infile))
    
    if p_message == 'playerdata':
        with open('playerData.json', 'r') as infile:
            return str(json.load(infile))
    
    
    if p_message == 'botlogs':
        with open('logData.txt', 'r') as infile:
            return infile.read()
    
    if p_message == 'clearlogs':
        with open('logData.txt', 'w') as outfile:
            outfile.write(f'<t:{int(time.time())}:f>Logs Cleared \n')
            return 'Cleared bot logs'
    
    if p_message == 'end':
        sys.exit()
    

    return 'Not a viable command!'