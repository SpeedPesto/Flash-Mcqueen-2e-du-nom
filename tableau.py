from flask import Flask, request
import threading

def setup_tableau(bot):
    CHANNEL_ID = 1467235315872694495

    app = Flask(__name__)

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

    @app.route("/tableau", methods=["POST"])
    def tableau():
        data = request.get_json()

        player = data.get("player", "Inconnu")
        blocks = data.get("blocks", [])

        size = 5  # largeur du tableau
        lines = []

        for i in range(0, len(blocks), size):
            line = "".join(blocks[i:i + size])
            lines.append(line)

        tableau = "\n".join(lines)

        msg = f"🎨 **Tableau de {player}**\n{tableau}"

        async def send():
            channel = await bot.fetch_channel(CHANNEL_ID)
            await channel.send(msg)

        bot.loop.create_task(send())
        return "ok", 200