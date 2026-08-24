import logging
import re

import discord
from discord.ext import commands

from config import roles

logger = logging.getLogger(__name__)


COURSE_ROLE_PATTERN = re.compile(r"^[A-Z]{2,4} \d{3,4}(?: (?:TA|Tracker))?$")


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
            *(role for role in ctx.guild.roles if COURSE_ROLE_PATTERN.match(role.name)),
        ):
            for member in role.members:
                await member.remove_roles(role)

        logger.info("Semester reset performed")
        await ctx.edit(content="Semester reset complete")


def setup(bot: commands.Bot):
    bot.add_cog(SemesterCommands(bot))
