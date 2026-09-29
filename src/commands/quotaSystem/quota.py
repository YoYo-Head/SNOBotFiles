import discord
from discord.ext import commands
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
        if interaction.user.id not in permsList:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        
        if reference.value == 1:
            userID = int(user.strip('<@!>'))
            member = interaction.guild.get_member(userID)
            if member is None or member.nick is None:
                await interaction.response.send_message("Couldn't find that member or their server nickname.", ephemeral=True)
                return
            userNick = member.nick
            if ']' not in userNick and userNick != interaction.user.name:
                await interaction.response.send_message(f'A unexpected error has occured dm <@{selfID}> for help')
                return
            elif ']' not in userNick:
                await interaction.response.send_message("A expected error has occured it is likely that the user hasn't used /verify yet")
                return
            else:
                userNick = userNick[userNick.find(']') + 2:].lower().strip()
        else:
            userNick = user

        
        if quota < 0:
            await interaction.response.send_message("Quota cannot be negative.", ephemeral=True)
            return
        
        with open('officerData.json', 'r') as infile:
            data = json.load(infile)
    
        
        if userNick in data:
            data[userNick] += quota
        else:
            data[userNick] = quota
        
        with open('officerData.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
            
        await interaction.response.send_message(f"Added {quota} QP to {userNick}'s quota.")

# Required setup function for Discord.py to load the cog
async def setup(bot):
    await bot.add_cog(QuotaSystems(bot))
