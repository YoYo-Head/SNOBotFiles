from http.client import responses



import discord
from discord.ext import commands
    
from sklearn import tree
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import SnoBot as SB
tk = SB.TOKEN
intentData = discord.Intents.all()
intentData.presences = False

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all(), application_id=1331105983090659399)
print(dir(discord))
print(dir(discord.ext))

async def send_message(message, user_message, is_private):
    try:
        await message.author.send(responses.handle_response(user_message)) if is_private else await message.channel.send(responses.handle_response(user_message))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    bot.run(SB.TOKEN)