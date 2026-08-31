from config import roles
from config.permissions import overwrites
from util.dataclasses import ChannelCategory, Course, TextChannel

COURSE_TRACKERS = ChannelCategory(name="Course Trackers")


def COURSE_CATEGORY(course: Course) -> ChannelCategory:
    course_role = roles.COURSE(course.name)
    tracker_role = roles.COURSE_TRACKER(course.name)
    ta_role = roles.TA(course.name)

    course_prefix = f"{course.subject.lower()}-{course.number}"

    return ChannelCategory(
        name=course.name,
        channels=[
            TextChannel(
                name=f"{course_prefix}-announcements",
                announcements=True,
                overwrites={
                    course_role: overwrites.READ_ONLY,
                    tracker_role: overwrites.READ_WRITE,
                    ta_role: overwrites.READ_WRITE,
                },
            ),
            TextChannel(
                name=f"{course_prefix}-reminders",
                overwrites={
                    course_role: overwrites.READ_ONLY,
                    tracker_role: overwrites.READ_WRITE,
                    ta_role: overwrites.READ_WRITE,
                },
            ),
            TextChannel(name=f"{course_prefix}-general"),
        ],
        overwrites={
            roles.EVERYONE: overwrites.DENY,
            roles.TRACKERS: overwrites.DENY,
            course_role: overwrites.VIEW,
            tracker_role: overwrites.VIEW,
            ta_role: overwrites.VIEW,
        },
    )
