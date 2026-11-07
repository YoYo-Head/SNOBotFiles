import discord
from discord.ext import commands
import asyncio
import time
import json
import config as cng
from .roblox_api import (
    RobloxAPIError,
    assign_user_role,
    get_group_rank,
    promote_user,
)


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
        with open('logData.txt', 'a') as logfile:
            logfile.write(f'<t:{int(time.time())}:f> {interaction.user.name}: change {rbx_id} {direction.name} {xp_value}\n')
        await interaction.response.defer()
        with open('playerData.json', 'r') as infile:
            data = json.load(infile)

        with open('rankData.json', 'r') as rankInfile:
            rankData = json.load(rankInfile)

        player_name = rbx_id
        user_id = None
        if rbx_id not in data:
            if direction.value != 1:
                await interaction.followup.send(f'{rbx_id} could not be found')
                return
            try:
                player_name, current_rank, user_id = await asyncio.to_thread(
                    get_group_rank, rbx_id
                )
            except RobloxAPIError as exc:
                await interaction.followup.send(f'Could not add {rbx_id}: {exc}')
                return
            if current_rank not in rankData:
                await interaction.followup.send(
                    f'Could not add {player_name}: their Roblox rank is not configured in rankData.json.'
                )
                return
            rbx_id = player_name.lower()
            data[rbx_id] = [rankData[current_rank][0], time.time(), current_rank]

        if direction.value == 1:
            data[rbx_id][0] += xp_value
        else:
            data[rbx_id][0] -= xp_value
        data[rbx_id][1] = time.time()
        current_rank = data[rbx_id][2]
        result = f'{xp_value} xp {directionVar} {player_name}!'

        rank_names = list(rankData)
        current_position = rank_names.index(current_rank)
        target_rank = current_rank
        for rank_name in rank_names:
            if rankData[rank_name][0] <= data[rbx_id][0]:
                target_rank = rank_name

        if rank_names.index(target_rank) > current_position:
            if user_id is not None:
                succeeded, promotion_result = await asyncio.to_thread(
                    assign_user_role, user_id, target_rank
                )
            else:
                succeeded, promotion_result = await asyncio.to_thread(
                    promote_user, player_name, target_rank
                )
            if succeeded:
                data[rbx_id][2] = target_rank
                result += f'\nAutomatically promoted to {target_rank}.'
            else:
                result += (
                    f'\nCould not automatically promote to {target_rank}: {promotion_result} '
                    'The promotion will be retried the next time /promos runs.'
                )

        with open('playerData.json', 'w') as outfile:
            json.dump(data, outfile, indent=2)
        await interaction.followup.send(result)
    
        
    
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
        with open('logData.txt', 'a') as logfile:
            logfile.write(f'<t:{int(time.time())}:f> {interaction.user.name}: promos\n')
        await interaction.response.defer()
        with open('playerData.json', 'r') as infile:
            data = json.load(infile)
        with open('rankData.json', 'r') as rankInfile:
            rankData = json.load(rankInfile)

        removed = []
        changed = {}
        previousRanks = {}
        rankPositions = {rank_name: index for index, rank_name in enumerate(rankData)}
        for item in data:
            if data[item][0] == 0:
                removed.append(item)
                continue
            elapsedTime = time.time() - data[item][1]
            data[item][1] = time.time()
            data[item][0] = data[item][0] - (rankData[data[item][2]][1] / 24 / 60 / 60 * elapsedTime)
            if data[item][0] < 0:
                data[item][0] = 0
            reverseKeyData = list(rankData.keys())
            reverseKeyData.reverse()
            for i in reverseKeyData:
                if rankData[i][0] <= data[item][0]:
                    if data[item][2] != i:
                        previousRanks[item] = data[item][2]
                        data[item][2] = i
                        changed[item] = i
                    break

        for item in removed:
            data.pop(item)

        messages = {}
        manual_changes = set()
        for item, new_rank in changed.items():
            old_rank = previousRanks[item]
            old_position = rankPositions.get(old_rank)
            new_position = rankPositions.get(new_rank)
            if old_position is not None and new_position is not None and new_position > old_position:
                succeeded, result = await asyncio.to_thread(promote_user, item, new_rank)
                if succeeded:
                    messages[item] = f'{item} was automatically promoted to {new_rank}.'
                else:
                    data[item][2] = old_rank
                    messages[item] = (
                        f'Could not automatically promote {item} to {new_rank}: {result} '
                        'The promotion will be retried the next time /promos runs.'
                    )
            else:
                messages[item] = f'{item} needs to be changed to {new_rank}'
                manual_changes.add(item)

        with open('playerData.json', 'w') as outfile:
            json.dump(data, outfile, indent=2)

        output = ""
        promotion_channel = discord.utils.get(interaction.guild.channels, id=promoChannel)
        for item, message in messages.items():
            if item in manual_changes:
                await promotion_channel.send(content=message, view=view)
            else:
                await promotion_channel.send(content=message)
            output += message + "\n"
        if output == "":
            output = "No promos available"
        output += f" <t:{int(time.time())}:R>"
        await interaction.followup.send(output)
    
    
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
        discord.app_commands.Choice(name='[OR-1] Initiative', value=1),
        discord.app_commands.Choice(name='[OR-2] Junior Operative', value=2),
        discord.app_commands.Choice(name='[OR-3] Operative', value=3),
        discord.app_commands.Choice(name='[OR-4] Senior Operative', value=4),
        discord.app_commands.Choice(name='[OR-5] Scuba Diver', value=5),
        discord.app_commands.Choice(name='[OR-6] Open Water Diver', value=6),
        discord.app_commands.Choice(name='[OR-7] Advanced Open Water Diver', value=7)
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
        with open('logData.txt', 'a') as logfile:
            logfile.write(f'<t:{int(time.time())}:f> {interaction.user.name}: promo {operation.name} {rbx_id} {rank.name}\n')

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
        discord.app_commands.Choice(name='[OR-1] Initiative', value=1),
        discord.app_commands.Choice(name='[OR-2] Junior Operative', value=2),
        discord.app_commands.Choice(name='[OR-3] Operative', value=3),
        discord.app_commands.Choice(name='[OR-4] Senior Operative', value=4),
        discord.app_commands.Choice(name='[OR-5] Scuba Diver', value=5),
        discord.app_commands.Choice(name='[OR-6] Open Water Diver', value=6),
        discord.app_commands.Choice(name='[OR-7] Advanced Open Water Diver', value=7)
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
        with open('logData.txt', 'a') as logfile:
            logfile.write(f'<t:{int(time.time())}:f> {interaction.user.name}: set_xp {rank.name} {operation.name} {xp_value}\n')
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
        discord.app_commands.Choice(name='[OR-1] Initiative', value=1),
        discord.app_commands.Choice(name='[OR-2] Junior Operative', value=2),
        discord.app_commands.Choice(name='[OR-3] Operative', value=3),
        discord.app_commands.Choice(name='[OR-4] Senior Operative', value=4),
        discord.app_commands.Choice(name='[OR-5] Scuba Diver', value=5),
        discord.app_commands.Choice(name='[OR-6] Open Water Diver', value=6),
        discord.app_commands.Choice(name='[OR-7] Advanced Open Water Diver', value=7)
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
    
