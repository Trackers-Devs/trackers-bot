import logging

import discord
from discord.ext import commands

from config import channels, roles
from util.autocomplete import course_autocomplete

logger = logging.getLogger(__name__)


class RequestCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    request = discord.SlashCommandGroup(
        name="request",
        description="Request special roles",
    )

    @request.command(
        name="ta-role",
        description="Request a Graduate or Undergraduate TA role for a course you're TAing for",
    )
    @discord.option(
        "course",
        description="Course you're TAing for",
        autocomplete=course_autocomplete,
    )
    @discord.option(
        "level",
        description="Your TA level",
        choices=["Graduate", "Undergraduate"],
    )
    @discord.option(
        "name",
        description="Your name, to verify your TA status",
    )
    async def request_ta_role(
        self,
        ctx: discord.ApplicationContext,
        course: str,
        level: str,
        name: str,
    ):
        await ctx.defer(ephemeral=True)

        course_role = discord.utils.get(ctx.guild.roles, name=course)
        if not course_role:
            await ctx.edit(content=f"{course} is not a course role")
            return

        await discord.utils.get(
            ctx.guild.text_channels, name=channels.SYS_COMMANDS.name
        ).send(
            f"{ctx.author.mention} ({name}) requested **{level} TA** for {course_role.mention}"
        )

        logger.info(f"{ctx.author} requested {level} TA role for {course_role.mention}")
        await ctx.edit(
            content=f"Your {level} TA request for {course_role.mention} has been submitted! A mod will review it shortly"
        )

    @request.command(
        name="course-tracker-role",
        description="Request the Course Tracker role for a course you want to track",
    )
    @discord.option(
        "course",
        description="Course you want to track",
        autocomplete=course_autocomplete,
    )
    async def request_course_tracker_role(
        self, ctx: discord.ApplicationContext, course: str
    ):
        await ctx.defer(ephemeral=True)

        course_role = discord.utils.get(ctx.guild.roles, name=course)
        if not course_role:
            await ctx.edit(content=f"{course} is not a course role")
            return

        await discord.utils.get(
            ctx.guild.text_channels, name=channels.SYS_COMMANDS.name
        ).send(
            f"{ctx.author.mention} requested **Course Tracker** role for {course_role.mention}"
        )

        logger.info(
            f"{ctx.author} requested Course Tracker role for {course_role.mention}"
        )
        await ctx.edit(
            content=f"Your Course Tracker request for {course_role.mention} has been submitted! A mod will review it shortly"
        )

    @request.command(
        name="graduated-role",
        description="Request Graduated role",
    )
    async def request_grad_role(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral=True)

        await ctx.author.add_roles(
            discord.utils.get(ctx.guild.roles, name=roles.GRADUATED.name)
        )

        logger.info(f"{ctx.author} was given Graduated role")
        await ctx.edit(content="Congrats on graduating!")


def setup(bot: commands.Bot):
    bot.add_cog(RequestCommands(bot))
