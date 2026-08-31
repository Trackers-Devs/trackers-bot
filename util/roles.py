from collections.abc import Callable

import discord

from config import roles
from util.dataclasses import Course, Role, RoleCategory
from util.regexes import COURSE_PATTERN, COURSE_TA_PATTERN, COURSE_TRACKER_PATTERN


def roles_between(
    guild: discord.Guild, upper: Role | RoleCategory, lower: Role | RoleCategory
) -> list[discord.Role]:
    upper_position = discord.utils.get(guild.roles, name=upper.name).position
    lower_position = discord.utils.get(guild.roles, name=lower.name).position

    return [
        role for role in guild.roles if lower_position < role.position < upper_position
    ]


async def create_course_roles(
    guild: discord.Guild, course: Course, add_ta: bool
) -> list[discord.Role]:
    async def position_role(
        role: discord.Role,
        anchor: Role | RoleCategory,
        is_sibling: Callable[[str], bool],
    ) -> None:
        roles = await guild.fetch_roles()

        siblings = sorted(
            (r for r in roles if is_sibling(r.name)), key=lambda r: r.name
        )
        sibling_ids = {r.id for r in siblings}

        anchor_position = discord.utils.get(roles, name=anchor.name).position
        lowest_position = min(
            (r.position for r in siblings if r.id != role.id), default=anchor_position
        )

        step = (
            anchor_position
            - max(
                (
                    r.position
                    for r in roles
                    if r.position < lowest_position and r.id not in sibling_ids
                ),
                default=lowest_position - (len(siblings) + 1) * 2,
            )
        ) / (len(siblings) + 1)

        positions = {
            r: round(anchor_position - step * (i + 1)) for i, r in enumerate(siblings)
        }

        await guild.edit_role_positions(positions=positions)

    course_role = discord.utils.get(guild.roles, name=course.name)
    if not course_role:
        course_role = await guild.create_role(name=course.name)
        await position_role(course_role, roles.categories.CLASSES, COURSE_PATTERN.match)

    tracker_role_name = roles.COURSE_TRACKER(course.name).name
    tracker_role = discord.utils.get(guild.roles, name=tracker_role_name)
    if not tracker_role:
        tracker_role = await guild.create_role(name=tracker_role_name)
        await position_role(
            tracker_role, roles.categories.COURSE_TRACKERS, COURSE_TRACKER_PATTERN.match
        )

    ta_role_name = roles.TA(course.name).name
    ta_role = discord.utils.get(guild.roles, name=ta_role_name)
    if not ta_role and add_ta:
        ta_role = await guild.create_role(name=ta_role_name)
        await position_role(
            ta_role, roles.categories.TEACHING_ASSISTANT, COURSE_TA_PATTERN.match
        )

    course_roles = [course_role, tracker_role]
    if ta_role:
        course_roles.append(ta_role)

    # REMOVE AFTER RUNNING ON EXISTING COURSES
    for role in course_roles:
        await role.edit(color=course.color, permissions=discord.Permissions.none())

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
