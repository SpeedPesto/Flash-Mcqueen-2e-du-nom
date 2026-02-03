import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from tableau import setup_tableau

load_dotenv()

#Infos perso
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Setup
setup_commands(bot)
setup_music(bot)
setup_events(bot)
setup_tableau(bot)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Commandes synchronisées : {len(synced)}")
    except Exception as e:
        print(e)

# --- Lance le bot ---
bot.run(TOKEN)
