from src import bot as main
import discord
from discord.ext import commands
import time
import json
import config as cng


bot = main.bot
tree = main.tree
guildID = main.guildID

promoChannel = cng.Promotions_Channel
HighRankID = cng.High_Commanding_Officer_ID
HighCommandID = cng.High_Commanding_Officer_ID
AdmiralID = cng.Main_Leaders_ID
selfID = cng.MyID

class ModSystems(commands.Cog):  # Inherit from commands.Cog
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance

    @discord.app_commands.command(name='change', description="Add or Subtract xp to a player's account")
    @discord.app_commands.describe(direction='Addition/Subtraction')
    @discord.app_commands.choices(direction=[
        discord.app_commands.Choice(name='Addition', value=1),
        discord.app_commands.Choice(name='Subtraction', value=2),
    ])
    async def changeCmd(self, interaction: discord.Interaction, rbx_id: str, direction: discord.app_commands.Choice[int], xp_value: int):
        userID = interaction.user.id
        idListOne = [item.id for item in discord.utils.get(interaction.guild.roles, id=HighRankID).members]
        idListTwo = [item.id for item in discord.utils.get(interaction.guild.roles, id=HighCommandID).members]
        idListThree = [item.id for item in discord.utils.get(interaction.guild.roles, id=AdmiralID).members]
        if (userID not in idListOne) and (userID not in idListTwo) and (userID not in idListThree) and (userID != selfID):
            await interaction.response.send_message('You are not authorized to run this command!')
            return
        if direction.value == 1:
            directionVar = 'added to'
        else:
            directionVar = 'subtracted from'
        rbx_id = rbx_id.lower()
        with open('logData.txt', 'r+') as logfile:
            logdata = logfile.read()
            logfile.seek(0, 0)
            logfile.write(logdata + f'<t:{int(time.time())}:f> {interaction.user.name}: change {rbx_id} {direction.name} {xp_value} \n')
        with open('playerData.json', 'r') as infile:
            data = json.load(infile)
        with open('playerData.json', 'w') as outfile:
            try:
                if direction.value == 1:
                    data[rbx_id] = [data[rbx_id][0] + xp_value, data[rbx_id][1], data[rbx_id][2]]
                else:
                    data[rbx_id] = [data[rbx_id][0] - xp_value, data[rbx_id][1], data[rbx_id][2]]
                result = f'{xp_value} xp {directionVar} {rbx_id}!'
            except:
                result = f'{rbx_id} could not be found'
            json.dump(data, outfile, indent=2)
        await interaction.response.send_message(result)
    
        
    
    @discord.app_commands.command(name="promos", description="Return all of the promotions/demotions that have changed")
    async def promos(self, interaction: discord.Interaction):
        button1 = discord.ui.Button(label='Resolve', style=discord.ButtonStyle.green)
            
        async def button1_callback(interaction):
            secondsLater = 60
            await interaction.response.edit_message(content=f"The user has been changed\tThis will delete <t:{round(time.time()) + secondsLater}:R>", view=None, delete_after=secondsLater)
            
        button1.callback = button1_callback
        view = discord.ui.View(timeout=None)
        view.add_item(button1)
        userID = interaction.user.id
        idListOne = [item.id for item in discord.utils.get(interaction.guild.roles, id=HighRankID).members]
        idListTwo = [item.id for item in discord.utils.get(interaction.guild.roles, id=HighCommandID).members]
        idListThree = [item.id for item in discord.utils.get(interaction.guild.roles, id=AdmiralID).members]
        if userID not in idListOne and userID not in idListTwo and userID not in idListThree and userID != selfID:
            await interaction.response.send_message('You are not authorized to run this command!')
            return
        with open('logData.txt', 'r+') as logfile:
            logdata = logfile.read()
            logfile.seek(0, 0)
            logfile.write(logdata + f'<t:{int(time.time())}:f> {interaction.user.name}: promos \n')
        with open('playerData.json', 'r') as infile:
            data = json.load(infile)
        with open('playerData.json', 'w') as outfile:
            removed = []
            changed = {}
            for item in data:
                if data[item][0] == 0:
                    removed.append(item)
                    continue
                elapsedTime = time.time() - data[item][1]
                data[item][1] = time.time()
                with open('rankData.json', 'r') as rankInfile:
                    rankData = json.load(rankInfile)
                    data[item][0] = data[item][0] - (rankData[data[item][2]][1] / 24 / 60 / 60 * elapsedTime)
                    if data[item][0] < 0:
                        data[item][0] = 0
                    reverseKeyData = list(rankData.keys())
                    reverseKeyData.reverse()
                    for i in reverseKeyData:
                        print(rankData[i])
                        print(data[item])
                        if rankData[i][0] <= data[item][0]:
                            if data[item][2] != i:
                                data[item][2] = i
                                changed[item] = i
                            break
            for item in removed:
                data.pop(item)
            json.dump(data, outfile, indent=2)
        output = ""
        for item in changed:
            await discord.utils.get(interaction.guild.channels, id=promoChannel).send(content=f'{item} needs to be changed to {changed[item]}', view=view)
            output = output + item + " -> " + changed[item] + "\n"
        if output == "":
            output = "No promos available"
        output = output + f" <t:{int(time.time())}:R>"
        await interaction.response.send_message(output)
    
    
        #take last time point and find elapsed time subtract from xp
        #set new time point
        #calculate roles
        #check who has changed
        #update playerData Var
        #dump new data
        #send response
    

    @discord.app_commands.command(name="promo", description="Add or remove a player manually to the list")
    @discord.app_commands.describe(operation='Addition/Subtraction')
    @discord.app_commands.choices(operation=[
        discord.app_commands.Choice(name='remove', value=1),
        discord.app_commands.Choice(name='add', value=2),
    ])
    @discord.app_commands.describe(rank='Addition/Subtraction')
    @discord.app_commands.choices(rank=[
        discord.app_commands.Choice(name='(TR-1) Seamen', value=1),
        discord.app_commands.Choice(name='(TR-2) Sailor First Class', value=2),
        discord.app_commands.Choice(name='(TR-3) Corporal', value=3),
        discord.app_commands.Choice(name='(TR-4) Corporal First Class', value=4),
        discord.app_commands.Choice(name='(TR-5) Corporal Major', value=5),
        discord.app_commands.Choice(name='(TR-6) Sergeant', value=6),
        discord.app_commands.Choice(name='(TR-7) First Sergeant', value=7),
       discord.app_commands.Choice(name='(TR-8) Brigader', value=8),
    ])
    async def promo(self, interaction: discord.Interaction, operation: discord.app_commands.Choice[int], rbx_id: str, rank: discord.app_commands.Choice[int]):
        userID = interaction.user.id
        idListOne = [item.id for item in discord.utils.get(interaction.guild.roles, id=HighRankID).members]
        idListTwo = [item.id for item in discord.utils.get(interaction.guild.roles, id=HighCommandID).members]
        idListThree = [item.id for item in discord.utils.get(interaction.guild.roles, id=AdmiralID).members]
        if userID not in idListOne and userID not in idListTwo and userID not in idListThree and userID != selfID:
           await interaction.response.send_message('You are not authorized to run this command!')
           return
        rbx_id = rbx_id.lower()
        with open('logData.txt', 'r+') as logfile:
            logdata = logfile.read()
            logfile.seek(0, 0)
            logfile.write(logdata + f'<t:{int(time.time())}:f> {interaction.user.name}: promo {operation.name} {rbx_id} {rank.name} \n')
        with open('playerData.json', 'r') as infile:
            data = json.load(infile)
        with open('playerData.json', 'w') as outfile:
            if operation.value == 1:
                try:
                    del data[rbx_id]
                    actionTaken = f'Removed {rbx_id} from LR/MR'
                except:
                    actionTaken = 'No match found'
            elif operation.value == 2:
                with open('rankData.json') as infile:
                    rankData = json.load(infile)
                rankSave = list(rankData.keys())[rank.value - 1]
                xp = rankData[rankSave][0] + 10
                data[rbx_id] = [xp, time.time(), rankSave]
                actionTaken = f'Added {rbx_id} to {rank.name}'
            json.dump(data, outfile, indent=2)
        await interaction.response.send_message(actionTaken)
    
    
    @discord.app_commands.command(name="set_xp", description="Change the requirements for ranks")
    @discord.app_commands.describe(rank='Rank to change')
    @discord.app_commands.choices(rank=[
        discord.app_commands.Choice(name='(TR-1) Seamen', value=1),
        discord.app_commands.Choice(name='(TR-2) Sailor First Class', value=2),
        discord.app_commands.Choice(name='(TR-3) Corporal', value=3),
        discord.app_commands.Choice(name='(TR-4) Corporal First Class', value=4),
        discord.app_commands.Choice(name='(TR-5) Corporal Major', value=5),
        discord.app_commands.Choice(name='(TR-6) Sergeant', value=6),
        discord.app_commands.Choice(name='(TR-7) First Sergeant', value=7),
        discord.app_commands.Choice(name='(TR-8) Brigader', value=8),
    ])
    @discord.app_commands.describe(operation='XP operation')
    @discord.app_commands.choices(operation=[
        discord.app_commands.Choice(name='degradation', value=1),
        discord.app_commands.Choice(name='minimum', value=2)
    ])
    async def set_degrade(self, interaction: discord.Interaction, rank: discord.app_commands.Choice[int], operation: discord.app_commands.Choice[int], xp_value: int):
        userID = interaction.user.id
        idList = [963893186621759568, 688807653182537747]
        if userID not in idList and userID != selfID:
            await interaction.response.send_message('You are not authorized to run this command!')
            return
        with open('logData.txt', 'r+') as logfile:
            logdata = logfile.read()
            logfile.seek(0, 0)
            logfile.write(logdata + f'<t:{int(time.time())}:f> {interaction.user.name}: set_xp {rank.name} {operation.name} {xp_value} \n')
        if operation.value == 1:
            with open('rankData.json', 'r') as infile:
               data = json.load(infile)
            with open('rankData.json', 'w') as outfile:
    
                data[list(data.keys())[rank.value - 1]][1] = xp_value
                json.dump(data, outfile, indent=2)
            await interaction.response.send_message(f"{rank.name}'s degradation has been set to {xp_value}")
        elif operation.value == 2:
            with open('rankData.json', 'r') as infile:
                data = json.load(infile)
            with open('rankData.json', 'w') as outfile:
    
                data[list(data.keys())[rank.value - 1]][0] = xp_value
                json.dump(data, outfile, indent=2)
            await interaction.response.send_message(f"{rank.name}'s requirement has been set to {xp_value}")
    
    @discord.app_commands.command(name="xp", description="See your current xp")
    async def see_xp(self, interaction: discord.Interaction):
        userNick = interaction.user.nick
        if userNick.find(']') == -1 and userNick != interaction.user.name:
            await interaction.response.send_message(f'A unexpected error has occured dm <@{selfID}> for help')
        elif userNick.find(']') == -1:
            await interaction.response.send_message("A expected error has occured try using <@298796807323123712>'s /verify command")
        else:
            userNick = userNick[userNick.find(']') + 2:].lower().strip()
            with open('playerData.json', 'r') as infile:
                data = json.load(infile)
                inList = False
                for i in data:
                    if i == userNick:
                        inList = True
                if inList == True:
                    await interaction.response.send_message(f'Your current xp is {int(data[userNick][0])}')
                else:
                    await interaction.response.send_message(f'The roblox name {userNick} could not be found in our database. You likely have not been introuduced into the xp system yet.')
    
    @discord.app_commands.command(name="see_xp", description="See a users xp")
    @discord.app_commands.describe(reference='XP operation')
    @discord.app_commands.choices(reference=[
        discord.app_commands.Choice(name='at [@]', value=1),
        discord.app_commands.Choice(name='rbx_id', value=2)
    ])
    async def check_xp(self, interaction: discord.Interaction, reference: discord.app_commands.Choice[int], user: str):
        userID = interaction.user.id
        idListOne = [item.id for item in discord.utils.get(interaction.guild.roles, id=HighRankID).members]
        idListTwo = [item.id for item in discord.utils.get(interaction.guild.roles, id=HighCommandID).members]
        idListThree = [item.id for item in discord.utils.get(interaction.guild.roles, id=AdmiralID).members]
        if userID not in idListOne and userID not in idListTwo and userID not in idListThree and userID != selfID:
            await interaction.response.send_message('You are not authorized to run this command!')
            return
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
        with open('playerData.json', 'r') as infile:
            data = json.load(infile)
            inList = False
            for i in data:
                if i == userNick:
                    inList = True
            if inList == True:
                if reference.value == 1:
                    await interaction.response.send_message(f"<@{userID}>'s current xp is {int(data[userNick][0])}")
                else:
                    await interaction.response.send_message(f"**{userNick}**'s current xp is {int(data[userNick][0])}")
            else:
                await interaction.response.send_message(f'The roblox name {userNick} could not be found in our database. You likely have not been introuduced into the xp system yet.')
    
    
    @discord.app_commands.command(name="rank_request", description="Request a LR/MR rank")
    @discord.app_commands.describe(rank='Rank to request')
    @discord.app_commands.choices(rank=[
        discord.app_commands.Choice(name='(TR-1) Seamen', value=1),
        discord.app_commands.Choice(name='(TR-2) Sailor First Class', value=2),
        discord.app_commands.Choice(name='(TR-3) Corporal', value=3),
        discord.app_commands.Choice(name='(TR-4) Corporal First Class', value=4),
        discord.app_commands.Choice(name='(TR-5) Corporal Major', value=5),
        discord.app_commands.Choice(name='(TR-6) Sergeant', value=6),
        discord.app_commands.Choice(name='(TR-7) First Sergeant', value=7),
        discord.app_commands.Choice(name='(TR-8) Brigader', value=8),
    ])
    async def rank_request(self, interaction: discord.Interaction, rank: discord.app_commands.Choice[int]):
        button1 = discord.ui.Button(label='Accept', style=discord.ButtonStyle.green)
        button2 = discord.ui.Button(label='Deny', style=discord.ButtonStyle.red)
        userID = interaction.user.id
    
        async def button1_callback(interaction):
            secondsLater = 2 * 60 * 60
            await interaction.response.edit_message(content=f"The rank {rank.name} has been accepted for <@{userID}>\tThis will delete <t:{round(time.time()) + secondsLater}:R>", view=None, delete_after=secondsLater)
            
        async def button2_callback(interaction):
            secondsLater = 60 * 60
            await interaction.response.edit_message(content=f"The rank {rank.name} has been denied for <@{userID}>\tThis will delete <t:{round(time.time()) + secondsLater}:R>", view=None, delete_after=secondsLater)
    
        button1.callback = button1_callback
        button2.callback = button2_callback
            
        view = discord.ui.View(timeout=None)
        view.add_item(button1)
        view.add_item(button2)
        await interaction.response.send_message(f'You have requested the rank {rank.name}')
        await discord.utils.get(interaction.guild.channels, id=promoChannel).send(content=f'<@{userID}> requests the rank {rank.name}', view=view)
    
        
async def setup(bot):
    await bot.add_cog(ModSystems(bot))   
    