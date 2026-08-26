import discord

from config import courses

_DESCRIPTION = "React below to unlock the respective course channels in the server."

CORE_CS = [
    discord.Embed(colour=courses.CORE_CS.color).set_image(
        url="attachment://core-cs.png"
    ),
    discord.Embed(colour=courses.CORE_CS.color, description=_DESCRIPTION),
]

TECH_ELECTIVE_1 = [
    discord.Embed(colour=courses.TECHNICAL_ELECTIVE.color).set_image(
        url="attachment://tech-elective-1.png"
    ),
    discord.Embed(colour=courses.TECHNICAL_ELECTIVE.color, description=_DESCRIPTION),
]

TECH_ELECTIVE_2 = [
    discord.Embed(colour=courses.TECHNICAL_ELECTIVE.color).set_image(
        url="attachment://tech-elective-2.png"
    ),
    discord.Embed(colour=courses.TECHNICAL_ELECTIVE.color, description=_DESCRIPTION),
]

MATH = [
    discord.Embed(colour=courses.MATH.color).set_image(url="attachment://math.png"),
    discord.Embed(colour=courses.MATH.color, description=_DESCRIPTION),
]

STAT = [
    discord.Embed(colour=courses.STAT.color).set_image(url="attachment://stat.png"),
    discord.Embed(colour=courses.STAT.color, description=_DESCRIPTION),
]

COURSE_EMBEDS = [
    CORE_CS,
    TECH_ELECTIVE_1,
    TECH_ELECTIVE_2,
    MATH,
    STAT,
]

# TODO

PERSONAL_EMBEDS = []

# TODO

COMMUNITY_EMBEDS = []
