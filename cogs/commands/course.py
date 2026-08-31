import logging

import discord
from discord.ext import commands

from config import courses
from util.channels import create_course_channels, delete_course_channels
from util.dataclasses import Course
from util.regexes import COURSE_EMOJI_PATTERN, COURSE_PATTERN
from util.roles import create_course_roles, delete_course_roles

logger = logging.getLogger(__name__)


async def _course_subject_autocomplete(ctx: discord.AutocompleteContext):
    subjects = set()
    for emoji in ctx.interaction.guild.emojis:
        match = COURSE_EMOJI_PATTERN.match(emoji.name)
        if match:
            subjects.add(match.group(1).upper())

    return sorted(
        subject for subject in subjects if subject.startswith((ctx.value or "").upper())
    )


async def _course_number_autocomplete(ctx: discord.AutocompleteContext):
    subject = (ctx.options.get("subject") or "").lower()

    numbers = set()
    for emoji in ctx.interaction.guild.emojis:
        match = COURSE_EMOJI_PATTERN.match(emoji.name)
        if match and (not subject or match.group(1) == subject):
            numbers.add(match.group(2))

    return sorted(number for number in numbers if number.startswith(ctx.value or ""))


async def _course_concentration_autocomplete(ctx: discord.AutocompleteContext):
    category = discord.utils.get(courses.CATEGORIES, name=ctx.options.get("category"))

    return [
        concentration.name
        for concentration in courses.CONCENTRATIONS.get(category, [])
        if concentration.name.upper().startswith((ctx.value or "").upper())
    ]


async def _course_autocomplete(ctx: discord.AutocompleteContext):
    return sorted(
        role.name
        for role in ctx.interaction.guild.roles
        if COURSE_PATTERN.match(role.name)
        and role.name.upper().startswith((ctx.value or "").upper())
    )


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
        autocomplete=_course_subject_autocomplete,
    )
    @discord.option(
        "number",
        description="Course number",
        autocomplete=_course_number_autocomplete,
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
        autocomplete=_course_concentration_autocomplete,
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
        autocomplete=_course_autocomplete,
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
