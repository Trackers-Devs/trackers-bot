import discord

from static import colors

INSTRUCTIONS = "React below to unlock the respective roles & channels in the server"

CORE_CS = [
    discord.Embed(color=colors.CORE_CS).set_image(url="attachment://core-cs.png"),
    discord.Embed(color=colors.CORE_CS, description=INSTRUCTIONS),
]

CS_ELECTIVE_1 = [
    discord.Embed(color=colors.CS_ELECTIVE).set_image(
        url="attachment://cs-elective-1.png"
    ),
    discord.Embed(color=colors.CS_ELECTIVE, description=INSTRUCTIONS),
]

CS_ELECTIVE_2 = [
    discord.Embed(color=colors.CS_ELECTIVE).set_image(
        url="attachment://cs-elective-2.png"
    ),
    discord.Embed(color=colors.CS_ELECTIVE, description=INSTRUCTIONS),
]

CS_ELECTIVE_3 = [
    discord.Embed(color=colors.CS_ELECTIVE).set_image(
        url="attachment://cs-elective-3.png"
    ),
    discord.Embed(color=colors.CS_ELECTIVE, description=INSTRUCTIONS),
]

MATH = [
    discord.Embed(color=colors.MATH).set_image(url="attachment://math.png"),
    discord.Embed(color=colors.MATH, description=INSTRUCTIONS),
]

STAT = [
    discord.Embed(color=colors.STAT).set_image(url="attachment://stat.png"),
    discord.Embed(color=colors.STAT, description=INSTRUCTIONS),
]

COURSE_EMBEDS = [
    CORE_CS,
    CS_ELECTIVE_1,
    CS_ELECTIVE_2,
    CS_ELECTIVE_3,
    MATH,
    STAT,
]

_COMMUNITY_DESCRIPTION = "\n\n".join(
    [
        "**Cook:** Want to learn to make healthy meals, interesting recipes, etc? Join the community of chefs and share your food with the world!",
        "**Entertainer:** Want to talk about TV/movies series, anime, books, sports, e-sports, and podcasts? Share your favorite entertainment with the community!",
        "**Exerciser:** Get access to the Fitness channels! Whether you're starting or a veteran, help the community together to stay healthy!",
        "**Gamer:** Gain access to the Gaming channels! Share your best gaming moments and highlights with the fellow Gamers!",
        "**Improver:** Life gets tough, but we are here to help you! Get the Improver role to talk about your struggles and learn to improve! YOU'RE NOT ALONE!",
        "**Musician:** Music creator? Music listener? Music lover in general? Learn to be a better musician and share your music with the community!",
    ]
)

COMMUNITY_EMBED = [
    discord.Embed(color=colors.COMMUNITY).set_image(url="attachment://community.png"),
    discord.Embed(color=colors.COMMUNITY, description=_COMMUNITY_DESCRIPTION).set_image(
        url="attachment://spacer.png"
    ),
    discord.Embed(color=colors.COMMUNITY, description=INSTRUCTIONS),
]
