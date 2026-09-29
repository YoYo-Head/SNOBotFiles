import discord
from discord.ext import commands
import config

class InfoSystems(commands.Cog):  # Inherit from commands.Cog
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance

    @discord.app_commands.command(name="ping", description="Pings the bot to see if it's online.")
    async def pingCMD(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"WebSocket latency: {round(self.bot.latency * 1000)} ms."
        )

    @commands.command()
    async def sync(self, ctx):
        if ctx.author.id == config.MyID:
            from src.bot import GUILD_ID
            synced = await self.bot.tree.sync(guild=discord.Object(id=GUILD_ID))
            await ctx.send(f'Synced {len(synced)} commands.')
        else:
            await ctx.send('You must be the owner to use this command!')

# Required setup function for Discord.py to load the cog
async def setup(bot):
    await bot.add_cog(InfoSystems(bot))
