import discord

from util.dataclasses import TextChannel


async def find_embed(
    bot: discord.Client, guild: discord.Guild, channel: TextChannel, marker: str
) -> discord.Message | None:
    channel = discord.utils.get(guild.text_channels, name=channel.name)

    async for message in channel.history():
        if message.author.id != bot.user.id:
            continue
        for embed in message.embeds:
            if embed.image and embed.image.url and marker in embed.image.url:
                return message

    return None
