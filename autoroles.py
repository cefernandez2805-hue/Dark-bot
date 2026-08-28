import discord
from discord.ext import commands

# Diccionario con el código del emoji y el nombre base del país
FLAGS = {
    "\U0001F1E8\U0001F1F4": "Colombia 🇨🇴",
    "\U0001F1F2\U0001F1FD": "México 🇲🇽",
    "\U0001F1EA\U0001F1F8": "España 🇪🇸",
    "\U0001F1FB\U0001F1EA": "Venezuela 🇻🇪",
    "\U0001F1F5\U0001F1F7": "Puerto Rico 🇵🇷",
    "\U0001F1EA\U0001F1E8": "Ecuador 🇪🇨",
    "\U0001F1E6\U0001F1F7": "Argentina 🇦🇷",
    "\U0001F1E8\U0001F1F1": "Chile 🇨🇱",
    "\U0001F1E7\U0001F1F4": "Bolivia 🇧🇴",
    "\U0001F1EC\U0001F1F9": "Guatemala 🇬🇹",
    "\U0001F1F8\U0001F1FB": "El Salvador 🇸🇻",
    "\U0001F1ED\U0001F1F3": "Honduras 🇭🇳",
    "\U0001F1F3\U0001F1EE": "Nicaragua 🇳🇮",
    "\U0001F1E8\U0001F1F7": "Costa Rica 🇨🇷",
    "\U0001F1F5\U0001F1E6": "Panamá 🇵🇦",
    "\U0001F1E8\U0001F1FA": "Cuba 🇨🇺",
    "\U0001F1E9\U0001F1F4": "República Dominicana 🇩🇴",
    "\U0001F1F5\U0001F1EA": "Perú 🇵🇪",
    "\U0001F1F5\U0001F1FE": "Paraguay 🇵🇾",
    "\U0001F1FA\U0001F1FE": "Uruguay 🇺🇾"
}

class AutoRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="autorol")
    @commands.has_permissions(administrator=True)
    async def autorol(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(
            title="🐻 | ¡ELIGE TU PAÍS!",
            description=(
                "🇨🇴 | **REACCIONA A ESTE MENSAJE CON LA BANDERA DE TU PAÍS**\n\n"
                "1. **Solo se puede seleccionar un país.**\n"
                "2. **Si te equivocas** y tienes que cambiar de país; primero **quita la reacción** y luego **vuelve a reaccionar** al país que deseas.\n"
                "3. Evita usar todos los emojis y así evitas bugs. Y listo, **disfruta del server con tu nuevo rol.** 🙋‍♂️"
            ),
            color=discord.Color.red()
        )
        embed.set_footer(text="Dark Autoroles | En caso tengas dudas o reportes con algún bug, abre un ticket.")

        msg = await ctx.send(embed=embed)
        for emoji in FLAGS.keys():
            await msg.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        emoji = str(payload.emoji)
        if emoji in FLAGS:
            guild = self.bot.get_guild(payload.guild_id)
            if not guild:
                return

            role_name = FLAGS[emoji]
            # Busca el rol en el servidor
            role = discord.utils.get(guild.roles, name=role_name)

            # Si el rol no existe, el bot lo crea automáticamente
            if not role:
                try:
                    role = await guild.create_role(name=role_name, mentionable=True)
                except discord.Forbidden:
                    print("El bot no tiene permisos para crear roles.")
                    return

            if role:
                member = payload.member or await guild.fetch_member(payload.user_id)
                if member:
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        emoji = str(payload.emoji)
        if emoji in FLAGS:
            guild = self.bot.get_guild(payload.guild_id)
            if not guild:
                return

            role_name = FLAGS[emoji]
            role = discord.utils.get(guild.roles, name=role_name)

            if role:
                member = await guild.fetch_member(payload.user_id)
                if member:
                    await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(AutoRoles(bot))
