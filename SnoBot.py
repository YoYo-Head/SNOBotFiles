from dotenv import load_dotenv
import asyncio
import os
from pathlib import Path

load_dotenv(Path(__file__).resolve().with_name(".env"), override=True)
TOKEN = os.getenv("DISCORD_TOKEN")
guildID = os.getenv("GUILD_ID")
applicationID = os.getenv("APPLICATION_ID")

async def run_bot():
    from src.bot import main
    await main()

if __name__ == "__main__":
    asyncio.run(run_bot())
