import discord
from discord.ext import commands

from config import channels
from static.embeds import reaction_roles
from util.embeds import find_embed


class EmbedCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    embed = discord.SlashCommandGroup(
        name="embed",
        description="Manage embeds",
        default_member_permissions=discord.Permissions(administrator=True),
    )

    @embed.command(
        name="get-course-roles",
        description="Send course reaction roles embed unless already exists",
    )
    async def get_course_roles(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral=True)

        channel = discord.utils.get(
            ctx.guild.text_channels, name=channels.GET_COURSE_ROLES.name
        )

        for banner, body in reaction_roles.COURSE_EMBEDS:
            filename = banner.image.url.removeprefix("attachment://")

            if await find_embed(self.bot, channel, filename):
                continue

            await channel.send(
                file=discord.File(f"static/embeds/images/{filename}"),
                embeds=[banner, body],
            )

        await ctx.edit(content="Done")


def setup(bot: commands.Bot):
    bot.add_cog(EmbedCommands(bot))
