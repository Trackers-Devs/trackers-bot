import re

# Roles
COURSE_ROLES_PATTERN = re.compile(r"^[A-Z]{2,4} \d{3,4}(?: (?:TA|Tracker))?$")
COURSE_PATTERN = re.compile(r"^[A-Z]{2,4} \d{3,4}$")
COURSE_TRACKER_PATTERN = re.compile(r"^[A-Z]{2,4} \d{3,4} Tracker$")
COURSE_TA_PATTERN = re.compile(r"^[A-Z]{2,4} \d{3,4} TA$")

# Emojis
COURSE_EMOJI_PATTERN = re.compile(r"^([a-z]{2,4})(\d{3,4})$")
