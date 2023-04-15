import datetime
from discord.ext import commands, tasks
from zoneinfo import ZoneInfo
from member_cog import TouchGrassMember


EST = ZoneInfo('US/Eastern')
daily_reset_time = datetime.time(hour=0, minute=0, tzinfo=EST)


class TouchGrass(commands.Cog):
    def __init__(self, bot, server_id, general, role):
        self.DAILY_THRESHOLD = 50
        self.SERVER_ID = server_id
        self.bot = bot
        self.general_channel = general
        self.daily_msg_count = {}
        self.touch_grass_role = role

        self.init_msg_counts()
        self.reset_daily_counts.start()

    # event listeners
    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author
        if member == self.bot.user:
            return
        print(f"Increasing {member}'s message count")
        # increase member's message count
        self.daily_msg_count[member] += 1
        # check if member already has role
        if member.get_role(self.touch_grass_role.id) != None:
            return
        # check if member is over daily threshold
        if self.daily_msg_count[member] > self.DAILY_THRESHOLD:
            print(f"{member} is over the daily threshold!")
            # give member role
            await member.add_roles(self.touch_grass_role)
            # add a new cog for the member
            await self.bot.add_cog(TouchGrassMember(self.bot, self.SERVER_ID, member, self.touch_grass_role))
            # send message
            await self.general_channel.send(f"<@{member.id}> go outside bruh")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("Adding new member to message count dictionary")
        # add a new entry in the message count dictionary
        self.daily_msg_count[member] = 0
    
    # background tasks
    @tasks.loop(time=daily_reset_time)
    async def reset_daily_counts(self):
        print("Daily message count reset!")
        for member in self.daily_msg_count:
            self.daily_msg_count[member] = 0

    # helpers
    def init_msg_counts(self):
        for member in self.bot.get_all_members():
            if member.bot:
                continue
            self.daily_msg_count[member] = 0
