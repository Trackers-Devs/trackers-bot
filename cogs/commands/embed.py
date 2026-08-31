import logging

import discord
from discord.ext import commands

from config import channels, courses, roles
from static.embeds import reaction_roles
from util.embeds import find_embed
from util.roles import roles_between

logger = logging.getLogger(__name__)


class EmbedCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    embed = discord.SlashCommandGroup(
        name="embed",
        description="Manage embeds",
        default_member_permissions=discord.Permissions(administrator=True),
    )

    @embed.command(
        name="get-course-roles",
        description="Send or update the course reaction roles embeds from the server's current course roles",
    )
    async def get_course_roles(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral="commands" not in ctx.channel.name)

        roles_by_category = {category: [] for category in courses.CATEGORIES}
        for role in roles_between(
            ctx.guild, roles.categories.CLASSES, roles.categories.BOTS
        ):
            subject, number = role.name.split(" ")
            category = next(
                (
                    c
                    for c in courses.CATEGORIES
                    if subject in c.subjects and (not c.numbers or number in c.numbers)
                ),
                None,
            )
            if category:
                roles_by_category[category].append(role)

        lines_by_category = {
            category: sorted(
                f"{emoji} — {role.mention}"
                for role in roles
                if (
                    emoji := discord.utils.get(
                        ctx.guild.emojis, name=role.name.replace(" ", "").lower()
                    )
                )
            )
            for category, roles in roles_by_category.items()
        }

        channel = discord.utils.get(
            ctx.guild.text_channels, name=channels.GET_COURSE_ROLES.name
        )

        logs = []

        for banner, body in reaction_roles.COURSE_EMBEDS:
            category = discord.utils.get(courses.CATEGORIES, color=body.color)

            lines = lines_by_category[category][:20]
            lines_by_category[category] = lines_by_category[category][20:]

            body.description = (
                reaction_roles.DESCRIPTION
                if not lines
                else "\n".join([reaction_roles.DESCRIPTION, "", *lines])
            )

            filename = banner.image.url.removeprefix("attachment://")
            label = (
                filename.removesuffix(".png")
                .replace("-", " ")
                .title()
                .replace("Cs", "CS")
                + " Courses embed"
            )

            message = await find_embed(
                self.bot, ctx.guild, channels.GET_COURSE_ROLES, filename
            )
            if message:
                if message.embeds[1].description == body.description:
                    logs.append(f"{label} unchanged")
                else:
                    await message.edit(embeds=[banner, body])
                    logs.append(f"Updated {label}")
            else:
                await channel.send(
                    file=discord.File(f"static/embeds/banners/{filename}"),
                    embeds=[banner, body],
                )
                logs.append(f"Sent {label}")

            logger.info(f"{logs[-1]} in #{channel.name}")

        await ctx.edit(content="\n".join(logs))


def setup(bot: commands.Bot):
    bot.add_cog(EmbedCommands(bot))
