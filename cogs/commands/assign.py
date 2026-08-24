import discord
from discord.ext import commands

from config import roles


class AssignCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    assign = discord.SlashCommandGroup(
        name="assign",
        description="Assign special roles to members",
        default_member_permissions=discord.Permissions(administrator=True),
    )

    @assign.command(
        name="grad-ta",
        description="Assign a member as Graduate TA for given course",
    )
    @discord.option(
        "member",
        description="Member to assign",
    )
    @discord.option("course", description="Course to assign TA role for")
    async def assign_graduate_ta(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member,
        course: discord.Role,
    ):
        await ctx.defer(ephemeral="commands" not in ctx.channel.name)

        for role in (
            discord.utils.get(ctx.guild.roles, name=role.name)
            for role in (
                roles.categories.TEACHING_ASSISTANT,
                roles.GRADUATE_TAS,
                roles.TA(course.name),
            )
        ):
            await member.add_roles(role)

        await ctx.edit(
            content=f"Assigned {member.mention} as Graduate TA for {course.mention}"
        )

    @assign.command(
        name="undergrad-ta",
        description="Assign a member as Undergraduate TA for given course",
    )
    @discord.option("member", description="Member to assign")
    @discord.option("course", description="Course to assign TA role for")
    async def assign_undergraduate_ta(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member,
        course: discord.Role,
    ):
        await ctx.defer(ephemeral="commands" not in ctx.channel.name)

        for role in (
            discord.utils.get(ctx.guild.roles, name=role.name)
            for role in (
                roles.categories.TEACHING_ASSISTANT,
                roles.UNDERGRADUATE_TAS,
                roles.TA(course.name),
            )
        ):
            await member.add_roles(role)

        await ctx.edit(
            content=f"Assigned {member.mention} as Undergraduate TA for {course.mention}"
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
