from dataclasses import dataclass

import discord

from static import colors


@dataclass(frozen=True)
class Role:
    name: str
    permissions: discord.Permissions = discord.Permissions.none()
    color: discord.Color = discord.Color.default()
    hoist: bool = False
    mentionable: bool = False


@dataclass(frozen=True)
class RoleCategory:
    name: str
    permissions: discord.Permissions = discord.Permissions.none()
    color: discord.Color = colors.CATEGORIES
    hoist: bool = False
    mentionable: bool = False

    def __post_init__(self):
        object.__setattr__(
            self,
            "name",
            f"\u2063{self.name:{'\u2002'}^{34}}{'\u2002' * 5}\u2063",
        )
