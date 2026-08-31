import discord

from config import channels
from util.dataclasses import Course
from util.regexes import COURSE_PATTERN


async def create_course_channels(guild: discord.Guild, course: Course) -> None:
    async def position_category_channel(
        course_category: discord.CategoryChannel,
    ) -> None:
        siblings = sorted(
            (
                c
                for c in guild.categories
                if c != course_category and COURSE_PATTERN.match(c.name)
            ),
            key=lambda c: c.name,
        )

        previous_category = next(
            (c for c in reversed(siblings) if c.name < course_category.name), None
        )
        if previous_category:
            await course_category.move(after=previous_category)
        elif siblings:
            await course_category.move(before=siblings[0])
        else:
            await course_category.move(
                before=discord.utils.get(
                    guild.categories, name=channels.categories.COURSE_TRACKERS.name
                )
            )

    category = channels.categories.COURSE_CATEGORY(course)

    category_overwrites = {}
    for role, overwrite in category.overwrites.items():
        role = discord.utils.get(guild.roles, name=role.name)
        if role:
            category_overwrites[role] = overwrite

    category_channel = discord.utils.get(guild.categories, name=category.name)
    if not category_channel:
        category_channel = await guild.create_category(
            name=category.name, overwrites=category_overwrites
        )
        await position_category_channel(category_channel)
    else:
        await category_channel.edit(overwrites=category_overwrites)

    for channel in category.channels:
        ch = discord.utils.get(category_channel.channels, name=channel.name)
        if not ch:
            ch = await guild.create_text_channel(
                channel.name, category=category_channel
            )
        ch = await ch.edit(sync_permissions=True)

        if channel.overwrites:
            channel_overwrites = dict(ch.overwrites)
            for role, overwrite in channel.overwrites.items():
                role = discord.utils.get(guild.roles, name=role.name)
                if role:
                    channel_overwrites[role] = overwrite

            ch = await ch.edit(overwrites=channel_overwrites)

        if channel.announcements and ch.type != discord.ChannelType.news:
            await ch.edit(type=discord.ChannelType.news)


async def delete_course_channels(
    guild: discord.Guild, course_role: discord.Role
) -> None:
    category_channel = discord.utils.get(guild.categories, name=course_role.name)
    if category_channel:
        for channel in category_channel.channels:
            await channel.delete()

        await category_channel.delete()
