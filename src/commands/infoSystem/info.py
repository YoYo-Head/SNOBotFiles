import append as main
import discord
import time
from discord.ext import commands

m = main.bot

bot = m.bot
tree = m.tree

def ms_time():
    # It is ms time
    return round(time.time() * 1000)

@bot.event
async def on_ready():
    channel = bot.get_channel(1273454633033142295)
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=m.guildID))
        print(f"Synced {len(synced)} commands to the guild.")   
    except Exception as e:
         print(f"Failed to sync commands: {e}")
    await channel.send('The bot is now **ONLINE** and ready to be used!')


@bot.tree.command(name="ping", description="Pings the bot to see if it's online.", guild=discord.Object(id=(m.guildID)))
async def pingCMD(interaction: discord.Interaction):
    pingList = []
    for pingNum in range(3):
        timerStart = ms_time()
        if pingNum == 0:
            await interaction.response.send_message(f'Ping {pingNum + 1} happening now!')

        else:
            await interaction.followup.send(f'Ping {pingNum + 1} happening now!')

        timerEnd = ms_time()
        pingTime = timerEnd - timerStart 
        await interaction.followup.send(f'Ping {pingNum + 1} took {pingTime} ms.')
        pingList.append(pingTime)

    ping1 = pingList[0]
    ping2 = pingList[1] 
    ping3 = pingList[2]

    pingAvg = (ping1 + ping2 + ping3) / 3

    await interaction.followup.send(f'**Average ping time was {pingAvg} ms.**')

@bot.command()
async def sync(ctx):
    print("sync command")
    if ctx.author.id == 1121379165195747328:
        await tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')