import logging

import discord
from discord.ext import commands

from config import channels, roles
from static.embeds import reaction_roles
from util.embeds import find_embed
from util.regexes import COURSE_ROLES_PATTERN

logger = logging.getLogger(__name__)


class SemesterCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    semester = discord.SlashCommandGroup(
        name="semester",
        description="Manage semester transitions",
        default_member_permissions=discord.Permissions(administrator=True),
    )

    @semester.command(
        name="reset",
        description="Perform server reset for a new semester",
    )
    async def reset(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral="commands" not in ctx.channel.name)

        for role in (
            *(
                discord.utils.get(ctx.guild.roles, name=role.name)
                for role in (
                    roles.categories.TEACHING_ASSISTANT,
                    roles.GRADUATE_TAS,
                    roles.UNDERGRADUATE_TAS,
                    roles.categories.COURSE_TRACKERS,
                    roles.COURSE_TRACKERS,
                )
            ),
            *(
                role
                for role in ctx.guild.roles
                if COURSE_ROLES_PATTERN.match(role.name)
            ),
        ):
            for member in role.members:
                await member.remove_roles(role)

        for banner, _ in reaction_roles.COURSE_EMBEDS:
            message = await find_embed(
                self.bot,
                ctx.guild,
                channels.GET_COURSE_ROLES,
                banner.image.url.removeprefix("attachment://"),
            )
            if not message:
                continue

            emojis = sorted(
                (
                    reaction.emoji
                    for reaction in message.reactions
                    if getattr(reaction.emoji, "name", None)
                ),
                key=lambda emoji: emoji.name,
            )

            await message.clear_reactions()
            for emoji in emojis:
                await message.add_reaction(emoji)

        logger.info("Semester reset performed")
        await ctx.edit(content="Semester reset complete")


def setup(bot: commands.Bot):
    bot.add_cog(SemesterCommands(bot))
