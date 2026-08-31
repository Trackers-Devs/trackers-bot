import discord

from config import courses
from util.regexes import COURSE_EMOJI_PATTERN, COURSE_PATTERN


async def course_subject_autocomplete(ctx: discord.AutocompleteContext):
    subjects = set()
    for emoji in ctx.interaction.guild.emojis:
        match = COURSE_EMOJI_PATTERN.match(emoji.name)
        if match:
            subjects.add(match.group(1).upper())

    return sorted(
        subject for subject in subjects if subject.startswith((ctx.value or "").upper())
    )


async def course_number_autocomplete(ctx: discord.AutocompleteContext):
    subject = (ctx.options.get("subject") or "").lower()

    numbers = set()
    for emoji in ctx.interaction.guild.emojis:
        match = COURSE_EMOJI_PATTERN.match(emoji.name)
        if match and (not subject or match.group(1) == subject):
            numbers.add(match.group(2))

    return sorted(number for number in numbers if number.startswith(ctx.value or ""))


async def course_concentration_autocomplete(ctx: discord.AutocompleteContext):
    category = discord.utils.get(courses.CATEGORIES, name=ctx.options.get("category"))

    return [
        concentration.name
        for concentration in courses.CONCENTRATIONS.get(category, [])
        if concentration.name.upper().startswith((ctx.value or "").upper())
    ]


async def course_autocomplete(ctx: discord.AutocompleteContext):
    return sorted(
        role.name
        for role in ctx.interaction.guild.roles
        if COURSE_PATTERN.match(role.name)
        and role.name.upper().startswith((ctx.value or "").upper())
    )
