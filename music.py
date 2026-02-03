import discord
from discord import app_commands
import yt_dlp
import asyncio

queues = {}

def setup_music(bot):

    async def play_next(interaction: discord.Interaction, guild_id):
        if queues[guild_id]:
            url = queues[guild_id].pop(0)

            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'noplaylist': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = info['url']  # c'est le flux direct que FFmpeg peut lire

            def after_play(error):
                asyncio.run_coroutine_threadsafe(play_next(interaction, guild_id), bot.loop)

            interaction.guild.voice_client.play(
                discord.FFmpegPCMAudio(audio_url, options='-vn'),
                after=after_play
            )
        else:
            try:
                await interaction.guild.voice_client.disconnect()
            except:
                pass

    @bot.tree.command(name="play", description="Joue une vidéo YouTube")
    @app_commands.describe(url="Lien YouTube de la vidéo")
    async def play_command(interaction: discord.Interaction, url: str):
        guild_id = interaction.guild.id
        if guild_id not in queues:
            queues[guild_id] = []

        if not interaction.guild.voice_client:
            if interaction.user.voice:
                channel = interaction.user.voice.channel
                await channel.connect()
            else:
                await interaction.response.send_message("Faut que tu sois connecté à un vok 👎", ephemeral=True)
                return

        # Récupérer le titre correctement
        ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'noplaylist': True, 'extract_flat': True}

        # Ajouter à la queue
        queues[guild_id].append(url)

        # Si rien n'est en train de jouer, lancer la lecture
        if not interaction.guild.voice_client.is_playing() and not interaction.guild.voice_client.is_paused():
            await interaction.response.send_message(f"OH LA VIDEO DE GOATTTTTTTTT, je la joue direct : **{url}** !")
            await play_next(interaction, guild_id)
        else:
            await interaction.response.send_message(f"OH LA VIDEO DE GOATTTTTTTTT, **{url}** a été ajoutée à la file d'attente !")

    @bot.tree.command(name="tagueule", description="Déconnecte le bot du vocal")
    async def leave_command(interaction: discord.Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("ok je ferme ma geule")
        else:
            await interaction.response.send_message("Je suis pas connecté à un vok, regarde un peu nan ?!")
