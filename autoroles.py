import discord
from discord.ext import commands

PAIS_ROLES = {
    "🇨🇴": "Colombia",
    "🇲🇽": "México",
    "🇪🇸": "España",
    "🇻🇪": "Venezuela",
    "🇵🇷": "Puerto Rico",
    "🇪🇨": "Ecuador",
    "🇦🇷": "Argentina",
    "🇨🇱": "Chile",
    "🇧🇴": "Bolivia",
    "🇬🇹": "Guatemala",
    "🇸🇻": "El Salvador",
    "🇭🇳": "Honduras",
    "🇳🇮": "Nicaragua",
    "🇨🇷": "Costa Rica",
    "🇵🇦": "Panamá",
    "🇨🇺": "Cuba",
    "🇩🇴": "República Dominicana",
    "🇵🇪": "Perú",
    "🇵🇾": "Paraguay",
    "🇺🇾": "Uruguay"
}

class AutoRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def autorol(self, ctx):
        await ctx.message.delete()
        
        embed = discord.Embed(
            title="🐻‍❄️ | ¡ELIGE TU PAÍS!",
            description=(
                "**🇨🇴 | REACCIONA A ESTE MENSAJE CON LA BANDERA DE TU PAÍS**\n\n"
                "1. **Solo se puede seleccionar un país.**\n"
                "2. **Si te equivocas** y tienes que cambiar de país; primero **quita la reacción** y luego **vuelve a reaccionar** al país que deseas.\n"
                "3. Evita usar todos los emojis y así evitas bugs. Y listo, **disfruta del server con tu nuevo rol. 🧑‍💻**"
            ),
            color=discord.Color.dark_red()
        )
        embed.set_footer(text="Dark Autoroles | En caso tengas dudas o reportes con algún bug, abre un ticket.")
        
        msg = await ctx.send(embed=embed)
        
        for emoji in PAIS_ROLES.keys():
            await msg.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        
        emoji = str(payload.emoji)
        if emoji in PAIS_ROLES:
            guild = self.bot.get_guild(payload.guild_id)
            role_name = PAIS_ROLES[emoji]
            role = discord.utils.get(guild.roles, name=role_name)
            
            if role:
                member = guild.get_member(payload.user_id)
                if member:
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        emoji = str(payload.emoji)
        if emoji in PAIS_ROLES:
            guild = self.bot.get_guild(payload.guild_id)
            role_name = PAIS_ROLES[emoji]
            role = discord.utils.get(guild.roles, name=role_name)
            
            if role:
                member = guild.get_member(payload.user_id)
                if member:
                    await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(AutoRoles(bot))

