from dataclasses import dataclass, field

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


@dataclass(frozen=True)
class TextChannel:
    name: str
    announcements: bool = False
    overwrites: dict[Role, discord.PermissionOverwrite] = field(default_factory=dict)


@dataclass(frozen=True)
class ChannelCategory:
    name: str
    channels: list[TextChannel] = field(default_factory=list)
    overwrites: dict[Role, discord.PermissionOverwrite] = field(default_factory=dict)


@dataclass(frozen=True)
class CourseCategory:
    name: str
    color: discord.Color
    subjects: tuple[str, ...] = ()
    numbers: frozenset[str] = frozenset()


@dataclass(frozen=True)
class CourseConcentration:
    name: str
    color: discord.Color


@dataclass(frozen=True)
class Course:
    subject: str
    number: str
    category: CourseCategory
    concentration: CourseConcentration | None = None

    @property
    def name(self) -> str:
        return f"{self.subject} {self.number}"

    @property
    def color(self) -> discord.Color:
        return self.concentration.color if self.concentration else self.category.color
