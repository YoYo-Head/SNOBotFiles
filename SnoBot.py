import subprocess
import os

print("SNO Bot is now launching!")
TOKEN = ''

if __name__ == "__main__":
    # Get the absolute path to bot.py relative to this file
    bot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'bot.py'))

    # Run bot.py
    subprocess.run(["python", bot_path])
    print("SNO Bor is now offline!")
