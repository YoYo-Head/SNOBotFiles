import discord
import time
from discord.ext import commands
from src import bot as m
from sklearn import tree

bot = m.bot
tree = m.tree

def ms_time():
    # It is ms time
    return round(time.time() * 1000)

class InfoSystems(commands.Cog):  # Inherit from commands.Cog
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance

    @discord.app_commands.command(name="ping", description="Pings the bot to see if it's online.")
    async def pingCMD(self, interaction: discord.Interaction):
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

    @commands.command()
    async def sync(self, ctx):
        print("sync command")
        if ctx.author.id == 1121379165195747328:
            await tree.sync()
            await ctx.send('Command tree synced.')
        else:
            await ctx.send('You must be the owner to use this command!')

# Required setup function for Discord.py to load the cog
async def setup(bot):
    await bot.add_cog(InfoSystems(bot))  # Register the cog