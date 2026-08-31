import logging

import discord
from discord.ext import commands

from config import courses
from util.autocomplete import (
    course_autocomplete,
    course_concentration_autocomplete,
    course_number_autocomplete,
    course_subject_autocomplete,
)
from util.channels import create_course_channels, delete_course_channels
from util.dataclasses import Course
from util.roles import create_course_roles, delete_course_roles

logger = logging.getLogger(__name__)


class CourseCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    course = discord.SlashCommandGroup(
        name="course",
        description="Manage courses",
        default_member_permissions=discord.Permissions(administrator=True),
    )

    @course.command(
        name="create",
        description="Create or update a course and its category, channels, roles, and reaction role",
    )
    @discord.option(
        "subject",
        description="Course subject",
        autocomplete=course_subject_autocomplete,
    )
    @discord.option(
        "number",
        description="Course number",
        autocomplete=course_number_autocomplete,
    )
    @discord.option(
        "category",
        description="Course category",
        choices=[
            discord.OptionChoice(name=category.name) for category in courses.CATEGORIES
        ],
    )
    @discord.option(
        "concentration",
        description="Course concentration",
        required=False,
        autocomplete=course_concentration_autocomplete,
    )
    @discord.option(
        "add-ta",
        parameter_name="add_ta",
        description="Create a TA role for this course",
        required=False,
    )
    async def create(
        self,
        ctx: discord.ApplicationContext,
        subject: str,
        number: str,
        category: str,
        concentration: str = None,
        add_ta: bool = False,
    ):
        await ctx.defer(ephemeral="commands" not in ctx.channel.name)

        category = discord.utils.get(courses.CATEGORIES, name=category)
        concentration = (
            discord.utils.get(
                courses.CONCENTRATIONS.get(category, []), name=concentration
            )
            if concentration
            else None
        )

        course = Course(
            subject=subject.upper(),
            number=number,
            category=category,
            concentration=concentration,
        )

        await create_course_roles(ctx.guild, course, add_ta)
        await create_course_channels(ctx.guild, course)

        logger.info(f"Created/updated {course.name} course")
        await ctx.edit(content=f"{course.name} course created/updated")

    @course.command(
        name="delete",
        description="Delete a course and its category, channels, and roles",
    )
    @discord.option(
        "course",
        description="Course to delete",
        autocomplete=course_autocomplete,
    )
    async def delete(self, ctx: discord.ApplicationContext, course: str):
        await ctx.defer(ephemeral="commands" not in ctx.channel.name)

        course_role = discord.utils.get(ctx.guild.roles, name=course)
        if not course_role:
            await ctx.edit(content=f"{course} is not a course role")
            return

        await delete_course_channels(ctx.guild, course_role)
        await delete_course_roles(ctx.guild, course_role)

        logger.info(f"Deleted {course_role.name} course")
        await ctx.edit(content=f"{course_role.name} course deleted")


def setup(bot: commands.Bot):
    bot.add_cog(CourseCommands(bot))
