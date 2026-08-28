import discord
from discord.ext import commands
from datetime import datetime
import os

intents = discord.Intents.default()
intents.members = True
intents.bans = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ID del canal de baneados
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
        title="🧔 Usuario Baneado",
        description=f"**{user.name}** ha sido baneado del servidor",
        color=discord.Color.from_rgb(231, 76, 60)
    )

    if user.avatar:
        embed.set_thumbnail(url=user.avatar.url)

    embed.add_field(name="👤 Usuario", value=f"<@{user.id}>\n{user.name}", inline=False)
    embed.add_field(name="🆔 ID", value=f"`{user.id}`", inline=False)
    embed.add_field(name="📅 Cuenta creada", value=f"<t:{int(user.created_at.timestamp())}:R>", inline=False)

    embed.set_footer(text="Dark", icon_url=guild.icon.url if guild.icon else None)
    embed.timestamp = datetime.utcnow()

    await canal.send(embed=embed)

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)

