import discord
from discord.ext import commands

FLAGS = {
    "🇨🇴": "Colombia 🇨🇴",
    "🇲🇽": "México 🇲🇽",
    "🇪🇸": "España 🇪🇸",
    "🇻🇪": "Venezuela 🇻🇪",
    "🇵🇷": "Puerto Rico 🇵🇷",
    "🇪🇨": "Ecuador 🇪🇨",
    "🇦🇷": "Argentina 🇦🇷",
    "🇨🇱": "Chile 🇨🇱",
    "🇧🇴": "Bolivia 🇧🇴",
    "🇬🇹": "Guatemala 🇬🇹",
    "🇸🇻": "El Salvador 🇸🇻",
    "🇭🇳": "Honduras 🇭🇳",
    "🇳🇮": "Nicaragua 🇳🇮",
    "🇨🇷": "Costa Rica 🇨🇷",
    "🇵🇦": "Panamá 🇵🇦",
    "🇨🇺": "Cuba 🇨🇺",
    "🇩🇴": "República Dominicana 🇩🇴",
    "🇵🇪": "Perú 🇵🇪",
    "🇵🇾": "Paraguay 🇵🇾",
    "🇺🇾": "Uruguay 🇺🇾"
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
                "🇳🇮  | **REACCIONA A ESTE MENSAJE CON LA BANDERA DE TU PAÍS**\n\n"
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
            role = discord.utils.get(guild.roles, name=role_name)

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
