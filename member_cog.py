import datetime
import time
from discord.ext import commands, tasks
from zoneinfo import ZoneInfo


reset_hour = datetime.datetime.now().hour
reset_min = datetime.datetime.now().minute -1
EST = ZoneInfo('US/Eastern')

# handle edge cases
if reset_min == -1:
    if reset_hour == 0:
        reset_hour = 23
    else:
        reset_hour -= 1
    reset_min = 59

role_reset_time = datetime.time(hour=reset_hour, minute=reset_min, tzinfo=EST)


class TouchGrassMember(commands.Cog):
    def __init__(self, bot, server_id, member, role):
        self.bot = bot
        self.server = bot.get_guild(server_id)
        self.member = member
        self.touch_grass_role = role
        self.day_countdown.start()

    @tasks.loop(time=role_reset_time)
    async def day_countdown(self):
        print(f"Removing {self.member}'s Needs To Touch Grass Role")
        await self.server.get_member(self.member.id).remove_roles(self.touch_grass_role)
        await self.bot.remove_cog(self.qualified_name)
        self.day_countdown.cancel()
