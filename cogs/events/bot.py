import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


class BotEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{self.bot.user.name} is ready and online!")
        logger.info(
            f"{self.bot.user.name} is connected to guilds: "
            f"{', '.join([guild.name for guild in self.bot.guilds])}"
        )

    @commands.Cog.listener()
    async def on_disconnect(self):
        logger.warning(f"{self.bot.user.name} disconnected from Discord")

    @commands.Cog.listener()
    async def on_resumed(self):
        logger.info(f"{self.bot.user.name} resumed session")


def setup(bot: commands.Bot):
    bot.add_cog(BotEvents(bot))
