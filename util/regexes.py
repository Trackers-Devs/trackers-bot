import re

# Roles
COURSE_ROLE_PATTERN = re.compile(r"^[A-Z]{2,4} \d{3,4}(?: (?:TA|Tracker))?$")

# Channels
REACTION_ROLES_CHANNEL_PATTERN = re.compile(r"^get-.+-roles$")
