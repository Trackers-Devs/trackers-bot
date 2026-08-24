from config.roles import categories  # noqa: F401
from static import colors
from util.dataclasses import Role

GRADUATE_TAS = Role(
    name="Graduate TAs",
    color=colors.GRADUATE_TAS,
    hoist=True,
    mentionable=True,
)

UNDERGRADUATE_TAS = Role(
    name="Undergraduate TAs",
    color=colors.UNDERGRADUATE_TAS,
    hoist=True,
    mentionable=True,
)


def TA(course: str):
    return Role(name=f"{course} TA")


COURSE_TRACKERS = Role(
    name="Course Trackers",
    color=colors.COURSE_TRACKERS,
    hoist=True,
    mentionable=True,
)


def COURSE_TRACKER(course: str):
    return Role(name=f"{course} Tracker")


TRACKERS = Role(
    name="Trackers",
    color=colors.TRACKERS,
    hoist=True,
    mentionable=True,
)
