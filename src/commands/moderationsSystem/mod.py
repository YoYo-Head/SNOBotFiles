from src import bot as m
import discord
from discord.ext import commands
import time
import json
import config as cng

class ModerationSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if permission == True:
            permission = ctx.author.guild_permissions.kick_members
            await member.kick(reason=reason)
            await ctx.send(f'{member.mention} has been kicked.')
        elif permission == False:
            await ctx.send(f'You do not have permission to kick members.')
        else:
            await ctx.send(f'An error occurred while trying to kick {member.mention}.')
            print(f'Error with kicking {member.mention}: {permission}')

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if permission == True:
            permission = ctx.author.guild_permissions.ban_members
            await member.ban(reason=reason)
            await ctx.send(f'{member.mention} has been banned.')
        elif permission == False:
            await ctx.send(f'You do not have permission to ban members.')
        else:
            await ctx.send(f'An error occurred while trying to ban {member.mention}.')
            print(f'Error with banning {member.mention}: {permission}')

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        if permission == True:
            permission = ctx.author.guild_permissions.ban_members
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f'{user.mention} has been unbanned.')
                    return
            await ctx.send(f'User {member} not found in the ban list.')
        elif permission == False:
            await ctx.send(f'You do not have permission to unban members.')
        else:
            await ctx.send(f'An error occurred while trying to unban {member}.')
            print(f'Error with unbanning {member}: {permission}')
