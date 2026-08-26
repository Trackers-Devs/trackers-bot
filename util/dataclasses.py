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


@dataclass(frozen=True)
class Channel:
    name: str


@dataclass(frozen=True)
class CourseCategory:
    name: str
    color: discord.Color


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

    def __post_init__(self):
        if not (
            2 <= len(self.subject) <= 4
            and self.subject.isalpha()
            and self.subject.isupper()
        ):
            raise ValueError(f"Unsupported course subject: {self.subject!r}")
        if not (self.number.isdigit() and 100 <= int(self.number) <= 9999):
            raise ValueError(f"Invalid course number: {self.number!r}")

    @property
    def name(self) -> str:
        return f"{self.subject} {self.number}"
