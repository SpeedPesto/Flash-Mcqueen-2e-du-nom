from flask import Flask, request
import threading

app = Flask(__name__)
bot_instance = None
CHANNEL_ID = 1467235315872694495


@app.route("/block", methods=["POST"])
def block():
    data = request.json
    msg = f"{data['player']} a posé {data['block']} en {data['pos']}"

    async def send():
        channel = await bot_instance.fetch_channel(CHANNEL_ID)
        await channel.send(msg)

    bot_instance.loop.create_task(send())
    return "ok"


@app.route("/tableau", methods=["POST"])
def tableau():
    data = request.get_json()
    player = data.get("player", "Inconnu")
    blocks = data.get("blocks", [])

    size = 5
    lines = []
    for i in range(0, len(blocks), size):
        line = "".join(blocks[i:i + size])
        lines.append(line)

    tableau_str = "\n".join(lines)
    msg = f"🎨 **Tableau de {player}**\n```\n{tableau_str}\n```"

    async def send():
        channel = await bot_instance.fetch_channel(CHANNEL_ID)
        await channel.send(msg)

    bot_instance.loop.create_task(send())
    return "ok", 200


def setup_tableau(bot):
    global bot_instance
    bot_instance = bot

    # Lance Flask une seule fois
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000), daemon=True).start()
    print("Serveur Flask démarré sur le port 5000")