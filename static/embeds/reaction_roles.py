import discord

from config import courses

DESCRIPTION = "React below to unlock the respective course channels in the server."

CORE_CS = [
    discord.Embed(color=courses.CORE_CS.color).set_image(
        url="attachment://core-cs.png"
    ),
    discord.Embed(color=courses.CORE_CS.color, description=DESCRIPTION),
]

CS_ELECTIVE_1 = [
    discord.Embed(color=courses.CS_ELECTIVE.color).set_image(
        url="attachment://cs-elective-1.png"
    ),
    discord.Embed(color=courses.CS_ELECTIVE.color, description=DESCRIPTION),
]

CS_ELECTIVE_2 = [
    discord.Embed(color=courses.CS_ELECTIVE.color).set_image(
        url="attachment://cs-elective-2.png"
    ),
    discord.Embed(color=courses.CS_ELECTIVE.color, description=DESCRIPTION),
]

CS_ELECTIVE_3 = [
    discord.Embed(color=courses.CS_ELECTIVE.color).set_image(
        url="attachment://cs-elective-3.png"
    ),
    discord.Embed(color=courses.CS_ELECTIVE.color, description=DESCRIPTION),
]

MATH = [
    discord.Embed(color=courses.MATH.color).set_image(url="attachment://math.png"),
    discord.Embed(color=courses.MATH.color, description=DESCRIPTION),
]

STAT = [
    discord.Embed(color=courses.STAT.color).set_image(url="attachment://stat.png"),
    discord.Embed(color=courses.STAT.color, description=DESCRIPTION),
]

COURSE_EMBEDS = [
    CORE_CS,
    CS_ELECTIVE_1,
    CS_ELECTIVE_2,
    CS_ELECTIVE_3,
    MATH,
    STAT,
]
