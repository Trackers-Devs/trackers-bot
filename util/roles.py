from collections.abc import Callable

import discord

from config import roles
from util.dataclasses import Course, Role, RoleCategory
from util.regexes import COURSE_PATTERN, COURSE_TA_PATTERN, COURSE_TRACKER_PATTERN


def get_roles_between(
    guild: discord.Guild, upper: Role | RoleCategory, lower: Role | RoleCategory
) -> list[discord.Role]:
    upper_position = discord.utils.get(guild.roles, name=upper.name).position
    lower_position = discord.utils.get(guild.roles, name=lower.name).position

    return [
        role for role in guild.roles if lower_position < role.position < upper_position
    ]


async def position_role(
    guild: discord.Guild,
    role: discord.Role,
    anchor: Role | RoleCategory,
    is_sibling: Callable[[str], bool],
) -> None:
    guild_roles = await guild.fetch_roles()

    siblings = sorted(
        (r for r in guild_roles if is_sibling(r.name)), key=lambda r: r.name
    )
    sibling_ids = {r.id for r in siblings}

    anchor_position = discord.utils.get(guild_roles, name=anchor.name).position
    lowest_position = min(
        (r.position for r in siblings if r.id != role.id), default=anchor_position
    )

    step = (
        anchor_position
        - max(
            (
                r.position
                for r in guild_roles
                if r.position < lowest_position and r.id not in sibling_ids
            ),
            default=lowest_position - (len(siblings) + 1) * 2,
        )
    ) / (len(siblings) + 1)

    await guild.edit_role_positions(
        positions={
            r: round(anchor_position - step * (i + 1)) for i, r in enumerate(siblings)
        }
    )


async def create_course_roles(
    guild: discord.Guild, course: Course, add_ta: bool
) -> list[discord.Role]:
    course_role = discord.utils.get(guild.roles, name=course.name)
    if not course_role:
        course_role = await guild.create_role(
            name=course.name,
            color=course.color,
            permissions=discord.Permissions.none(),
        )
        await position_role(
            guild, course_role, roles.categories.CLASSES, COURSE_PATTERN.match
        )

    tracker = roles.COURSE_TRACKER(course.name)
    tracker_role = discord.utils.get(guild.roles, name=tracker.name)
    if not tracker_role:
        tracker_role = await guild.create_role(
            name=tracker.name,
            color=course.color,
            permissions=discord.Permissions.none(),
        )
        await position_role(
            guild,
            tracker_role,
            roles.categories.COURSE_TRACKERS,
            COURSE_TRACKER_PATTERN.match,
        )

    ta = roles.TA(course.name)
    ta_role = discord.utils.get(guild.roles, name=ta.name)
    if not ta_role and add_ta:
        ta_role = await guild.create_role(
            name=ta.name,
            color=course.color,
            permissions=discord.Permissions.none(),
        )
        await position_role(
            guild, ta_role, roles.categories.TEACHING_ASSISTANT, COURSE_TA_PATTERN.match
        )

    course_roles = [course_role, tracker_role]
    if add_ta:
        course_roles.append(ta_role)

    return course_roles


async def delete_course_roles(guild: discord.Guild, course_role: discord.Role) -> None:
    tracker_role = discord.utils.get(
        guild.roles, name=roles.COURSE_TRACKER(course_role.name).name
    )
    if tracker_role:
        await tracker_role.delete()

    ta_role = discord.utils.get(guild.roles, name=roles.TA(course_role.name).name)
    if ta_role:
        await ta_role.delete()

    await course_role.delete()
