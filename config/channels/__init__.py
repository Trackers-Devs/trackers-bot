from config.channels import categories  # noqa: F401
from util.dataclasses import TextChannel

# Role Claim Service
GET_COURSE_ROLES = TextChannel(name="get-course-roles")
GET_PERSONAL_ROLES = TextChannel(name="get-personal-roles")
GET_COMMUNITY_ROLES = TextChannel(name="get-community-roles")

# Sys Channels
SYS_COMMANDS = TextChannel(name="sys-commands")
