from http.client import responses
import asyncio
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

bot = commands.Bot(command_prefix='$', intents=intentData, application_id=1375429887288016896)
guildID = SB.guildID

print(dir(discord))
print(dir(discord.ext))

@bot.event
async def on_ready():
    channel = bot.get_channel(1273454633033142295)
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=guildID))
        print(f"Synced {len(synced)} commands to the guild.")   
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    await channel.send('The bot is now **ONLINE** and ready to be used!')

async def send_message(message, user_message, is_private):
    try:
        await message.author.send(responses.handle_response(user_message)) if is_private else await message.channel.send(responses.handle_response(user_message))
    except Exception as e:
        print(e)

async def main():
    
    await bot.load_extension("commands.infoSystem.info")
    print("Information Systems loaded!")

    #await bot.load_extension("commands.moderationsSystem.mod")
    #print("Moderation System loaded!")

    await bot.load_extension("commands.promotionSystem.promo")
    print("Promotions System loaded!")

    await bot.start(SB.TOKEN)

if __name__ == "__main__":
    asyncio.run(main())