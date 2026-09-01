import discord
from discord.ext import commands

from config import roles
from util.regexes import COURSE_TA_PATTERN
from util.roles import position_role


class AssignCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    assign = discord.SlashCommandGroup(
        name="assign",
        description="Assign special roles to members",
        default_member_permissions=discord.Permissions(administrator=True),
    )

    @assign.command(
        name="ta-role",
        description="Assign a member as Graduate or Undergraduate TA for given course",
    )
    @discord.option("member", description="Member to assign")
    @discord.option("course", description="Course to assign TA role for")
    @discord.option(
        "level",
        description="TA level",
        choices=["Graduate", "Undergraduate"],
    )
    async def assign_ta_role(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member,
        course: discord.Role,
        level: str,
    ):
        await ctx.defer(ephemeral="commands" not in ctx.channel.name)

        ta = roles.TA(course.name)
        ta_role = discord.utils.get(ctx.guild.roles, name=ta.name)
        if not ta_role:
            ta_role = await ctx.guild.create_role(
                name=ta.name,
                color=course.colors.primary,
                permissions=discord.Permissions.none(),
            )
            await position_role(
                ctx.guild,
                ta_role,
                roles.categories.TEACHING_ASSISTANT,
                COURSE_TA_PATTERN.match,
            )

        level_role = discord.utils.get(
            ctx.guild.roles,
            name=(
                roles.GRADUATE_TAS if level == "Graduate" else roles.UNDERGRADUATE_TAS
            ).name,
        )

        for role in (
            level_role,
            discord.utils.get(
                ctx.guild.roles, name=roles.categories.TEACHING_ASSISTANT.name
            ),
            ta_role,
        ):
            await member.add_roles(role)

        await ctx.edit(
            content=f"Assigned {member.mention} as {level} TA for {course.mention}"
        )

    @assign.command(
        name="course-tracker",
        description="Assign a member as Course Tracker for given course",
    )
    @discord.option("member", description="Member to assign")
    @discord.option("course", description="Course to assign tracker role for")
    async def assign_course_tracker(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member,
        course: discord.Role,
    ):
        await ctx.defer(ephemeral="commands" not in ctx.channel.name)

        for role in (
            discord.utils.get(ctx.guild.roles, name=role.name)
            for role in (
                roles.categories.COURSE_TRACKERS,
                roles.COURSE_TRACKERS,
                roles.COURSE_TRACKER(course.name),
            )
        ):
            await member.add_roles(role)

        await ctx.edit(
            content=f"Assigned {member.mention} as Course Tracker for {course.mention}"
        )


def setup(bot: commands.Bot):
    bot.add_cog(AssignCommands(bot))
