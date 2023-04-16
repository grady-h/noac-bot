import datetime
from discord.ext import commands, tasks
from zoneinfo import ZoneInfo

EST = ZoneInfo('US/Eastern')
daily_reset_time = datetime.time(hour=0, minute=0, tzinfo=EST)

class TouchGrass(commands.Cog):
    def __init__(self, bot, general, role, member, msg_counts):
        self.DAILY_THRESHOLD = 5
        self.bot = bot
        self.general_channel = general
        self.touch_grass_role = role
        self.touch_grass_member = member
        self.member_msg_count = msg_counts
        self.daily_msg_count = {}
        self.must_go_outside = []

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
        self.member_msg_count[member] += 1
        self.daily_msg_count[member] += 1

        # DAILY THRESHOLD CHECK
        # check if member is over daily threshold and hasn't already been called out
        if self.daily_msg_count[member] > self.DAILY_THRESHOLD and not member in self.must_go_outside:
            print(f"{member} is over the daily threshold!")
            # send message
            await self.general_channel.send(f"<@{member.id}> go outside bruh")
            # add to must go outside list
            self.must_go_outside.append(member)

        # TOUCH GRASS ROLE CHECK
        # check if member already has role
        if member.get_role(self.touch_grass_role.id) != None:
            return
        # check if member has more messages than current touch grass member
        member_count = self.member_msg_count[member]
        current_max = self.member_msg_count[self.touch_grass_member]
        if member_count > current_max:
            # remove role from current max member
            await self.touch_grass_member.remove_roles(self.touch_grass_role)
            # make author new touch grass member
            await member.add_roles(self.touch_grass_role)
            self.touch_grass_member = member
            # send message
            await self.general_channel.send(f"<@{self.touch_grass_member.id}> is the new non-grass toucher with {member_count} messages. PLEASE go outside dawg")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("Adding new member to message count dictionaries")
        # add a new entry in the message count dictionaries
        self.member_msg_count[member] = 0
        self.daily_msg_count[member] = 0

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print("Removing old member from message count dictionaries")
        del self.member_msg_count[self.touch_grass_member]
        del self.daily_msg_count[self.touch_grass_member]
        if member == self.touch_grass_member:
            print("Transferring Touch Grass role to second place member")
            # find member with next highest message count
            self.touch_grass_member = list(self.member_msg_count.keys())[0]
            for member in self.member_msg_count:
                if self.member_msg_count[member] > self.member_msg_count[self.touch_grass_member]:
                    self.touch_grass_member = member
            # transfer role
            await self.touch_grass_member.add_roles(self.touch_grass_role)

    # background task
    @tasks.loop(time=daily_reset_time)
    async def reset_daily_counts(self):
        print("Daily message count reset!")
        # reset counts
        for member in self.daily_msg_count:
            self.daily_msg_count[member] = 0
        # clear the must go outside member list
        self.must_go_outside = []

    # helper
    def init_msg_counts(self):
        for member in self.member_msg_count:
            self.daily_msg_count[member] = 0
            print(member, self.member_msg_count[member])
