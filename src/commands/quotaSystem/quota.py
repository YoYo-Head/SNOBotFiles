from src import bot as main
import discord
from discord.ext import commands
import time
import json
import config as cng

selfID = cng.MyID
LeaderID = cng.Main_Leaders_ID

permsList = [selfID, LeaderID]

class QuotaSystems(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='add-quota', description='Add QP to an officer.')
    @discord.app_commands.choices(reference=[
        discord.app_commands.Choice(name='at [@]', value=1),
        discord.app_commands.Choice(name='rbx_id', value=2)
        ])
    async def add_quota(self, interaction: discord.Interaction, reference: discord.app_commands.Choice[int], user: str, quota: int):
        print('stage zero')
        if interaction.user.id not in permsList:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        print('stage one')
        
        if reference.value == 1:
            userID = int(user[2:-1])
            userNick = discord.utils.get(interaction.guild.members, id=userID).nick
            if userNick.find(']') == -1 and userNick != interaction.user.name:
                await interaction.response.send_message(f'A unexpected error has occured dm <@{selfID}> for help')
                return
            elif userNick.find(']') == -1:
                await interaction.response.send_message("A expected error has occured it is likely that the user hasn't used /verify yet")
                return
            else:
                userNick = userNick[userNick.find(']') + 2:].lower().strip()
        else:
            userNick = user

        print('stage two')
        
        if quota < 0:
            await interaction.response.send_message("Quota cannot be negative.", ephemeral=True)
            return
        
        with open('officerData.json', 'r') as infile:
            print('reading')
            data = json.load(infile)
            print('reading complete')
    
        
        if userNick in data:
            data[userNick] += quota
        else:
            data[userNick] = quota
        
        with open('officerData.json', 'w') as outfile:
            print('writing')
            json.dump(data, outfile, indent=4)
            print('writing complete')
        
        await interaction.response.send_message(f"Added {quota} QP to {userNick}'s quota.")

# Required setup function for Discord.py to load the cog
async def setup(bot):
    await bot.add_cog(QuotaSystems(bot))  # Register the cog