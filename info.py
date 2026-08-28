import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    @commands.has_permissions(administrator=True)
    async def info(self, ctx):
        await ctx.message.delete()

        # EMBED 1: INFORMACIÓN DE ROLES Y NIVELES
        embed_roles = discord.Embed(
            title="💠 │ Información de Roles",
            description=(
                "**Roles de Nivel**\n"
                "En este apartado podrás encontrar la información de los roles del servidor que "
                "se te otorgan mediante vas subiendo de nivel (siendo activo en el chat), junto a los "
                "beneficios que estos llevan. Si tienes alguna duda extra puedes abrir un ticket en el canal de <#1542667687753289748>\n\n"
                "El bot de nivelación que se utiliza es **@Arcane#7800**, el prefijo que se utiliza es `/`, "
                "para poder ver tu nivel solo usa `/rank` en el canal de <#1542662996621262898>\n\n"
                "⚪ │ **Nivel 10**\n"
                "└ Podrás enviar imágenes por <#1542662791754678303>\n\n"
                "⚪ │ **Nivel 100**\n"
                "└ Tendrás acceso a un canal de texto y voz privados (VIP)\n\n"
                "**Booster**\n"
                "Beneficios que adquieres al boostear el servidor, reclámalos en <#1542667687753289748>\n"
                "• Color personalizados VIP o normal.\n"
                "• Canal de texto y voz privado.\n"
                "• Enviar multimedia por todos los canales del servidor.\n"
                "• Subir 5 niveles en el servidor.\n"
                "• Participar en sorteos exclusivos como subs al canal de Dark u otros en <#1542662158356058123>"
            ),
            color=discord.Color.from_rgb(220, 20, 60)
        )

        # EMBED 2: REDES SOCIALES DE DARK
        embed_redes = discord.Embed(
            title="📸 │ Información de Redes Sociales",
            description=(
                "Todas estas redes sociales son oficiales y legítimas de **Dark**. Queda prohibido "
                "cualquier intento de falsificación o difamación hacia cualquiera de estas mismas.\n\n"
                "⚪ │ **TikTok**\n"
                "[Dark TikTok](https://www.tiktok.com/@dark_oficial_cdg?_r=1&_t=ZS-99Gq3IqcHwd)\n\n"
                "⚪ │ **Discord**\n"
                "discord de la gang de SB de Dark\n"
                "└---> https://discord.gg/ZfSjbrdh7"
            ),
            color=discord.Color.from_rgb(220, 20, 60)
        )

        await ctx.send(embed=embed_roles)
        await ctx.send(embed=embed_redes)

async def setup(bot):
    await bot.add_cog(Info(bot))

