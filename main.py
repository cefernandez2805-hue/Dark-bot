import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands
from datetime import datetime

# Servidor HTTP en segundo plano para Render
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot activo")

def start_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    server.serve_forever()

threading.Thread(target=start_web_server, daemon=True).start()

# Configuración del Bot
intents = discord.Intents.default()
intents.members = True
intents.bans = True

bot = commands.Bot(command_prefix="!", intents=intents)

ID_CANAL_BANEADOS = 1542659452191117403

@bot.event
async def on_ready():
    print(f"Bot de Dark conectado exitosamente como {bot.user}")

@bot.event
async def on_member_ban(guild, user):
    canal = bot.get_channel(ID_CANAL_BANEADOS)
    if not canal:
        return

    embed = discord.Embed(
        title="⛔ Usuario Baneado",
        description=f"**{user.name}** ha sido baneado del servidor.",
        color=discord.Color.from_rgb(231, 76, 60)
    )

    if user.avatar:
        embed.set_thumbnail(url=user.avatar.url)

    embed.add_field(name="👤 Usuario", value=f"<@{user.id}>\n({user.name})", inline=False)
    embed.add_field(name="🆔 ID", value=f"`{user.id}`", inline=False)
    embed.add_field(name="📅 Cuenta creada", value=f"<t:{int(user.created_at.timestamp())}:R>", inline=False)

    embed.set_footer(text="Dark", icon_url=guild.icon.url if guild.icon else None)
    embed.timestamp = datetime.utcnow()

    await canal.send(embed=embed)

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
