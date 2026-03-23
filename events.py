import random
import string

mots_cars = [
    "cars", "flash mcqueen", "mcqueen", "vitesse", "rapide", "turbo",
    "accélération", "course", "drift", "virage", "pneu", "piste", "flash"
]

sus_messages = ["nigga", "nigger", "nigg", "negro", "neggro", "nazi", "niga", "nigg", "négro", "ngro"]
sus_gifs = [
    "https://giphy.com/gifs/confused-futurama-suspicious-ANbD1CCdA3iI8",
    "https://giphy.com/gifs/dexter-suspicious-aniflicks-21VTFJTEr1x9ortvO3",
    "https://giphy.com/gifs/showtime-hbo-prime-puOukoEvH4uAw",
    "https://giphy.com/gifs/moodman-monkey-side-eye-sideeye-H5C8CevNMbpBqNqFjl",
    "https://giphy.com/gifs/sus-suspicious-meme-ewq2ZiQMWvGffIMRTz",
    "https://giphy.com/gifs/FugzOfficial-fug-fugz-fugzofficial-jN2ZFtiPyFxwVaaBbo",
    "https://giphy.com/gifs/chicken-suspicious-despicable-me-WiVvi66FqT2bpym6R8"
]
sus_answers = [
    "Hmm- tu t'es trompé de mot je suppose...",
    "Ton clavier à ripper ? ça arrive souvent..",
    "C'est pas ce que tu voulais dire je crois..",
    "t'es sur de ce mot là ?"
]

cat_messages = ["to catch it!"]

def setup_events(bot):

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        # Cars reactions
        if any(mot in message.content.lower() for mot in mots_cars):
            if random.randint(1, 3) != 1:
                await message.add_reaction("🚗")
            else:
                for lettre in ["🇨", "🇦", "🇷", "🇸"]:
                    await message.add_reaction(lettre)

        # Sus filter
        if any(mot in message.content.lower() for mot in sus_messages):
            random_sus_gif = random.choice(sus_gifs)
            random_sus_message = random.choice(sus_answers)
            assemblage = f"{random_sus_gif}\n{random_sus_message}"
            await message.reply(assemblage)

        if any(mot in message.content.lower() for mot in cat_messages):
            await message.delete()
            return

        # "quoi" -> "feur"
        contenu = message.content.strip()
        if contenu:
            contenu_nettoye = "".join(c for c in contenu if c not in string.whitespace + string.punctuation)
            if contenu_nettoye.lower().endswith("quoi"):
                if random.randint(1, 2) != 1:
                    await message.reply("FEUR !! 🤣🤣")
                else:
                    await message.reply("COUBEH !! 🤣🤣")

        await bot.process_commands(message)
