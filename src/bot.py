import asyncio
import discord
from discord.ext import commands
import SnoBot as SB

APPLICATION_ID = int(SB.applicationID) if SB.applicationID else 1331105983090659399
GUILD_ID = int(SB.guildID) if SB.guildID else 1273454632382759046
STATUS_CHANNEL_ID = 1273454633033142295

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents, application_id=APPLICATION_ID)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (application {bot.application_id})")
    try:
        guild = discord.Object(id=GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands to guild {GUILD_ID}.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    channel = bot.get_channel(STATUS_CHANNEL_ID)
    if channel is not None:
        await channel.send('The bot is now **ONLINE** and ready to be used!')

async def main():

    await bot.load_extension("src.commands.infoSystem.info")
    print("Information Systems loaded!")

    await bot.load_extension("src.commands.moderationsSystem.mod")
    print("Moderation System loaded!")

    await bot.load_extension("src.commands.promotionSystem.promo")
    print("Promotions System loaded!")

    await bot.load_extension("src.commands.quotaSystem.quota")
    print("Quota System loaded!")

    print("Commands currently registered:")

    for command in bot.tree.get_commands():
        print(f" - {command.name}")

    print(f"Total commands: {len(bot.tree.get_commands())}")
    if not SB.TOKEN:
        raise RuntimeError("DISCORD_TOKEN is not set. Set it in the environment or .env file.")

    async with bot:
        await bot.start(SB.TOKEN)
if __name__ == "__main__":
    asyncio.run(main())

