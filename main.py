import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask, request
import asyncio
from dotenv import load_dotenv
import threading
import os

load_dotenv()

#Infos perso
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1467235315872694495

# Intents
intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)
loop = asyncio.get_event_loop()

app = Flask(__name__)

# Quand le bot est prêt
@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Commandes synchronisées : {len(synced)}")
    except Exception as e:
        print(e)

def run_flask():
    app.run(host="0.0.0.0", port=5000)
threading.Thread(target=run_flask).start()

@app.route("/block", methods=["POST"])
def block():
    data = request.json
    msg = f"{data['player']} a posé {data['block']} en {data['pos']}"

    async def send():
        channel = await bot.fetch_channel(CHANNEL_ID)
        await channel.send(msg)

    # Utiliser le loop du bot
    bot.loop.create_task(send())
    return "ok"

# /ninja
@bot.tree.command(name="ninja", description="go")
async def salut(interaction: discord.Interaction):
    await interaction.response.send_message("goo")


# --- Lance le bot ---
bot.run(TOKEN)
