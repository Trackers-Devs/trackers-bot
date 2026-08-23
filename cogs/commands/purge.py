import logging

import discord
from discord.ext import commands

from config.roles.categories import (
    BOTS,
    CLASSES,
    COURSE_TRACKERS,
    PERSONAL,
    TEACHING_ASSISTANT,
)
from util import RoleMgr

logger = logging.getLogger(__name__)


class PurgeCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    purge = discord.SlashCommandGroup(
        name="purge",
        default_member_permissions=discord.Permissions(administrator=True),
    )

    @purge.command(
        name="course-trackers",
        description="Purge Course Trackers",
    )
    async def purge_course_trackers(self, ctx: discord.ApplicationContext):
        guild: discord.Guild = ctx.guild
        await ctx.respond("Purging Course Trackers...", ephemeral=True)

        course_tracker_role_category = discord.utils.get(
            guild.roles, name=COURSE_TRACKERS.name
        )
        course_tracker_role = discord.utils.get(guild.roles, name="Course Trackers")

        await RoleMgr.purge(
            [
                course_tracker_role_category,
                course_tracker_role,
                *RoleMgr.get_between(
                    guild.roles,
                    course_tracker_role_category,
                    discord.utils.get(guild.roles, name=TEACHING_ASSISTANT.name),
                ),
            ]
        )

        logger.info(f"Member @{ctx.author.name} purged Course Trackers")
        await ctx.edit(content="Purged Course Trackers")

    @purge.command(
        name="tas",
        description="Purge TAs",
    )
    async def purge_tas(self, ctx: discord.ApplicationContext):
        guild: discord.Guild = ctx.guild
        await ctx.respond("Purging TAs...", ephemeral=True)

        ta_role_category = discord.utils.get(guild.roles, name=TEACHING_ASSISTANT.name)
        graduate_ta_role = discord.utils.get(guild.roles, name="Graduate TAs")
        undergraduate_ta_role = discord.utils.get(guild.roles, name="Undergraduate TAs")

        await RoleMgr.purge(
            [
                ta_role_category,
                graduate_ta_role,
                undergraduate_ta_role,
                *RoleMgr.get_between(
                    guild.roles,
                    ta_role_category,
                    discord.utils.get(guild.roles, name=PERSONAL.name),
                ),
            ]
        )

        logger.info(f"Member @{ctx.author} purged TAs")
        await ctx.edit(content="Purged TAs")

    @purge.command(
        name="trackers",
        description="Purge Trackers",
    )
    async def purge_trackers(self, ctx: discord.ApplicationContext):
        guild: discord.Guild = ctx.guild
        await ctx.respond("Purging Trackers...", ephemeral=True)

        await RoleMgr.purge(
            RoleMgr.get_between(
                guild.roles,
                discord.utils.get(guild.roles, name=CLASSES.name),
                discord.utils.get(guild.roles, name=BOTS.name),
            )
        )

        logger.info(f"Member @{ctx.author.name} purged Trackers")
        await ctx.edit(content="Purged Trackers")


def setup(bot: commands.Bot):
    bot.add_cog(PurgeCommands(bot))
