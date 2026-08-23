import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("main")

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logger.critical("DISCORD_TOKEN not found in environment.")
        exit(1)

    bot = commands.Bot(
        command_prefix="!",
        intents=discord.Intents.all(),
        allowed_mentions=discord.AllowedMentions.none(),
    )

    for path in Path("cogs").rglob("*.py"):
        if path.stem != "__init__":
            bot.load_extension(".".join(path.with_suffix("").parts))

    bot.run(DISCORD_TOKEN)
