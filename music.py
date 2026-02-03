import discord
from discord import app_commands
import yt_dlp
import asyncio

queues = {}


def setup_music(bot):
    async def play_next(guild_id):
        guild = bot.get_guild(guild_id)
        if not guild or not guild.voice_client:
            return

        if queues.get(guild_id):
            url = queues[guild_id].pop(0)

            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'noplaylist': True,
                'no_warnings': True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    audio_url = info['url']
                    title = info.get('title', 'Titre inconnu')

                def after_play(error):
                    if error:
                        print(f"Erreur de lecture : {error}")
                    # Utiliser asyncio pour planifier la prochaine chanson
                    fut = asyncio.run_coroutine_threadsafe(play_next(guild_id), bot.loop)

                guild.voice_client.play(
                    discord.FFmpegPCMAudio(audio_url, options='-vn'),
                    after=after_play
                )
                print(f"🎵 Lecture en cours : {title}")
            except Exception as e:
                print(f"❌ Erreur lors de la lecture : {e}")
                await play_next(guild_id)
        else:
            # File d'attente vide, déconnexion après 2 minutes
            await asyncio.sleep(120)
            if guild.voice_client and not guild.voice_client.is_playing():
                await guild.voice_client.disconnect()

    @bot.tree.command(name="play", description="Joue une vidéo YouTube")
    @app_commands.describe(url="Lien YouTube de la vidéo")
    async def play_command(interaction: discord.Interaction, url: str):
        guild_id = interaction.guild.id
        if guild_id not in queues:
            queues[guild_id] = []

        # Connexion au vocal
        if not interaction.guild.voice_client:
            if interaction.user.voice:
                channel = interaction.user.voice.channel
                await channel.connect()
            else:
                await interaction.response.send_message("Faut que tu sois connecté à un vok 👎", ephemeral=True)
                return

        # Récupérer le titre
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'extract_flat': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', url)
        except:
            title = url

        # Ajouter à la queue
        queues[guild_id].append(url)

        # Si rien n'est en train de jouer, lancer la lecture
        if not interaction.guild.voice_client.is_playing() and not interaction.guild.voice_client.is_paused():
            await interaction.response.send_message(f"OH LA VIDEO DE GOATTTTTTTTT, je la joue direct : **{title}** !")
            await play_next(guild_id)
        else:
            await interaction.response.send_message(
                f"OH LA VIDEO DE GOATTTTTTTTT, **{title}** a été ajoutée à la file d'attente !")

    @bot.tree.command(name="tagueule", description="Déconnecte le bot du vocal")
    async def leave_command(interaction: discord.Interaction):
        guild_id = interaction.guild.id
        if guild_id in queues:
            queues[guild_id].clear()

        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("ok je ferme ma geule")
        else:
            await interaction.response.send_message("Je suis pas connecté à un vok, regarde un peu nan ?!")