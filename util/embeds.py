import discord


async def find_embed(
    bot: discord.Client, channel: discord.TextChannel, filename: str
) -> discord.Message | None:
    async for message in channel.history():
        if message.author.id != bot.user.id:
            continue
        for embed in message.embeds:
            if embed.image and embed.image.url and filename in embed.image.url:
                return message

    return None
