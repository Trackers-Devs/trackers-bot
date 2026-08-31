import logging

import discord
from discord.ext import commands

from config import channels, courses, roles
from static import embeds
from util.embeds import find_embed
from util.roles import roles_between

logger = logging.getLogger(__name__)


class EmbedCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    embed = discord.SlashCommandGroup(
        name="embed",
        description="Send/resend embeds",
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

        for banner, body in embeds.reaction_roles.COURSE_EMBEDS:
            category = discord.utils.get(courses.CATEGORIES, color=body.color)

            lines = lines_by_category[category][:20]
            lines_by_category[category] = lines_by_category[category][20:]

            body.description = (
                embeds.reaction_roles.INSTRUCTIONS
                if not lines
                else "\n".join([embeds.reaction_roles.INSTRUCTIONS, "", *lines])
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

    @embed.command(
        name="get-community-roles",
        description="Send or update the community reaction roles embed from the server's current community roles",
    )
    async def get_community_roles(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral="commands" not in ctx.channel.name)

        channel = discord.utils.get(
            ctx.guild.text_channels, name=channels.GET_COMMUNITY_ROLES.name
        )

        lines = sorted(
            f"{emoji} — {role.mention}"
            for role in roles_between(
                ctx.guild, roles.categories.COMMUNITY, roles.categories.CLASSES
            )
            if (
                emoji := discord.utils.get(
                    ctx.guild.emojis, name=role.name.replace(" ", "").lower()
                )
            )
        )

        banner, info, body = embeds.reaction_roles.COMMUNITY_EMBED
        body.description = (
            embeds.reaction_roles.INSTRUCTIONS
            if not lines
            else "\n".join([embeds.reaction_roles.INSTRUCTIONS, "", *lines])
        )

        filename = banner.image.url.removeprefix("attachment://")

        message = await find_embed(
            self.bot, ctx.guild, channels.GET_COMMUNITY_ROLES, filename
        )
        if message:
            if message.embeds[2].description == body.description:
                log = "Community roles embed unchanged"
            else:
                await message.edit(embeds=[banner, info, body])
                log = "Updated community roles embed"
        else:
            await channel.send(
                files=[
                    discord.File(f"static/embeds/banners/{filename}"),
                    discord.File("static/embeds/banners/spacer.png"),
                ],
                embeds=[banner, info, body],
            )
            log = "Sent community roles embed"

        logger.info(f"{log} in #{channel.name}")
        await ctx.edit(content=log)


def setup(bot: commands.Bot):
    bot.add_cog(EmbedCommands(bot))
