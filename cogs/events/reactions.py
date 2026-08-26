import discord
from discord.ext import commands

from util.reaction_roles import find_reaction_role
from util.regexes import REACTION_ROLES_CHANNEL_PATTERN


class ReactionEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        channel = guild.get_channel(payload.channel_id)
        if not channel or not REACTION_ROLES_CHANNEL_PATTERN.match(channel.name):
            return

        message = await channel.fetch_message(payload.message_id)

        role = find_reaction_role(guild, message.embeds[1], str(payload.emoji))
        if not role:
            return

        member = payload.member or guild.get_member(payload.user_id)
        if not member or member.bot:
            return

        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        channel = guild.get_channel(payload.channel_id)
        if not channel or not REACTION_ROLES_CHANNEL_PATTERN.match(channel.name):
            return

        message = await channel.fetch_message(payload.message_id)

        role = find_reaction_role(guild, message.embeds[1], str(payload.emoji))
        if not role:
            return

        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return

        await member.remove_roles(role)


def setup(bot: commands.Bot):
    bot.add_cog(ReactionEvents(bot))
