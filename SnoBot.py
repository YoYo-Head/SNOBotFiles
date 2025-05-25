from dotenv import load_dotenv
import subprocess
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

guildID = os.getenv("GUILD_ID")

pythonV = os.path.join(os.path.dirname(__file__), 'venv', 'Scripts', 'python.exe')
if __name__ == "__main__":
    # Get the absolute path to bot.py relative to this file
    bot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'bot.py'))

    print("SNO Bot is now launching!")

    # Run bot.py
    subprocess.run([pythonV, bot_path])

    # Once all has been run/shut down
    print("SNO Bor is now offline!")
