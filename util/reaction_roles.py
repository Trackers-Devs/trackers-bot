import discord


def find_reaction_role(
    guild: discord.Guild, embed: discord.Embed, emoji: str
) -> discord.Role | None:
    for line in embed.description.splitlines():
        if not line.startswith(emoji):
            continue

        return guild.get_role(int(line.split(" — ", 1)[-1].strip("<@&>")))

    return None
