import discord
import os
import random

cars_repliques = [
    "Ka-chow !", "Je suis la vitesse !", "À l’époque on ne cherchait pas à gagner du temps, on prenait le temps…",
    "- Rapide comme l’éclair ? \n- Puissant comme la foudre !", "Le plus important c’est de savoir d’où l’on vient pas de savoir où l’on va.",
    "Tourner à droite pour aller à gauche j’ai essayé et il s’est passé quelque chose d’incroyable je suis allé à droite.",
    "Si tu crois que j’ai remplacé ton carburant par une de mes essences bio, t’es a coté d’tes plaques man !",
    "Flotter comme une Cadillac, piquer comme une BM !", "Plus rapide que l’éclair, je suis Flash McQueen !",
    "Ka-chow ! Flash McQueen !"
]

def setup_commands(bot):

    @bot.tree.command(name="salut", description="Le bot te répond Ka-chow")
    async def salut(interaction: discord.Interaction):
        await interaction.response.send_message("Ka-chow 🚗💨")

    @bot.tree.command(name="cars", description="Envoie une image de Cars aléatoire")
    async def cars_command(interaction: discord.Interaction):
        random_replique = random.choice(cars_repliques)
        folder_path = "imgs/cars"
        images = os.listdir(folder_path)
        random_image = random.choice(images)
        image_path = os.path.join(folder_path, random_image)
        image = discord.File(image_path, filename=random_image)
        await interaction.response.send_message(content=random_replique, file=image)
