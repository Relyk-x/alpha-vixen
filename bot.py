import discord
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime
import datetime
import time
import random
import requests
import os
import sys

#import config
try:
    import config
except:
    sys.exit("'config.py' not found! Please add it and try again.")

#colors
red = discord.Status.dnd
yellow = discord.Status.idle
green = discord.Status.online
none = discord.Status.invisible

#bot emoji
p = "<:point:548835150838890497>"
on = "<:online:548835125706883072>"
off = "<:offline:548833521255579648>"
ide = "<:idle:548835110279970827>"
dnds = "<:dnd:548835091007143971>"

#time
now = datetime.datetime.now()
diff = datetime.datetime(now.year, 2, 13) - \
    datetime.datetime.today()  # Days until Christmas

#client
bot = commands.Bot(command_prefix=",", status=yellow, activity=discord.Game(name="v0.2.0 | Booting...", type=3))

#command removal 
bot.remove_command("help")

#start up
@bot.event
async def on_ready():
    print("Ready to go!")
    print(f"Serving: {len(bot.guilds)} guilds.")
    await bot.change_presence(status=green, activity=discord.Game(name="v0.2.0 | ,help", type=3))

@bot.listen()
async def on_message(message):
    if "<@257784039795064833>" in message.content:
        await message.add_reaction(discord.utils.get(bot.emojis, name="blobsweat"))

#error commands
@bot.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="red_cross_mark"))
        await ctx.send(f"Command is not found. Please check commands and try again.")
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="red_cross_mark"))
        await ctx.send(f"Command is forbidden. You are lacking permissions.")
        return
    elif isinstance(error, commands.NotOwner):
        await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="red_cross_mark"))
        await ctx.send(f"Command is forbidden. You are not the owner.")
        return
    elif isinstance(error, commands.CheckFailure):
        await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="red_cross_mark"))
        await ctx.send(f"Command is nsfw. Please set channel to nsfw and try again.")
        return

#ping latency command
@bot.command()
async def ping(ctx):
	await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
	#await message.channel.startTyping();
	ping_ = bot.latency
	ping = round(ping_ * 1000)
	await ctx.send(f"My ping is {ping}ms")

#ban user command
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member:discord.User = None, reason = None):
    await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
    #await ctx.trigger_typing(ctx.message.channel)
    if member == None or member == ctx.author:
        await ctx.send("You can't ban yourself!")
        return
    if reason == None:
        reason = "No reason at all!"
    message = f"You have been banned from {ctx.guild.name} for {reason}!"
    await member.send(message)
    await ctx.guild.ban(member)
    await ctx.send(f"{member} was banned!")

#kick user command
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.User = None, reason = None):
    await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
    #await ctx.trigger_typing(ctx.message.channel)
    if member == None or member == ctx.author:
        await ctx.send("You can't kick yourself!")
        return
    if reason == None:
        reason = "No reason at all!"
    message = f"You have been kicked from {ctx.guild.name} for {reason}!"
    await member.send(message)
    await ctx.guild.kick(member)
    await ctx.send(f"{member} was kicked")

#purge up to 100 messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx):
    channel = ctx.message.channel
    deleted = await channel.purge(limit=100)
    emb = discord.Embed(title=":warning: Purge", description=f"Purged **{len(deleted)}** general message(s) from the channel", color=0xe02f5a)
    await ctx.send(embed=emb, delete_after=10.0)

#clear specific amount of messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, messages:int):
    channel = ctx.message.channel
    deleted = await channel.purge(limit=messages)
    emb = discord.Embed(title=":warning: Clear", description=f"Cleared **{len(deleted)}** general message(s) from the channel", color=0xe02f5a)
    await ctx.send(embed=emb, delete_after=10.0)

#delete specific amount of messages from mentioned member
@bot.command()
@commands.has_permissions(manage_messages=True)
async def delete(ctx, messages:int, m:discord.Member):
    def is_member(message):
        return m == ctx.message.author
    channel = ctx.message.channel
    deleted = await channel.purge(limit=messages, check=is_member)
    emb = discord.Embed(title=":warning: Delete", description=f"Deleted **{len(deleted)}** of {ctx.member.name}'s message(s) from the channel", color=0xe02f5a)
    await ctx.send(embed=emb, delete_after=10.0)

#clean specific amount of messages from bot
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clean(ctx, messages:int):
    def is_bot(message):
        return ctx.guild.me == ctx.message.author
    channel = ctx.message.channel
    deleted = await channel.purge(limit=messages, check=is_bot)
    emb = discord.Embed(title=":warning: Clean", description=f"Cleaned **{len(deleted)}** bot message(s) from the channel", color=0xe02f5a)
    await ctx.send(embed=emb, delete_after=10.0)

#count server members
@bot.command()
async def count(ctx):
	#await ctx.trigger_typing(ctx.message.channel)
	bots = 0
	members = 0
	total = 0
	on_line = len([I for I in ctx.message.guild.members if I.status is discord.Status.online])
	on_idle = len([I for I in ctx.message.guild.members if I.status is discord.Status.idle])
	on_dnd = len([I for I in ctx.message.guild.members if I.status is discord.Status.dnd])
	off_line = len([I for I in ctx.message.guild.members if I.status is discord.Status.offline])
	for x in ctx.message.guild.members:
	 if x.bot == True:
	  bots += 1
	  total += 1
	 else:
	  members += 1
	  total += 1
	await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
	emb = discord.Embed(title=":information_source: Server Count",color=0xe02f5a)
	emb.add_field(name="Status", value=f"{on}Online: {on_line}\n{ide}Idle: {on_idle}\n{dnds}Do Not Disturb: {on_dnd}\n{off}Offline: {off_line}", inline=True)
	emb.add_field(name="Server",value=f"{p}Members: {total}\n{p}Users: {members}\n{p}Bots: {bots}", inline=True)
	emb.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url) 
	await ctx.send(embed=emb)

#server information
@bot.command()
async def server(ctx):
	bots = 0
	members = 0
	total = 0
	on_line = len([I for I in ctx.message.guild.members if I.status is discord.Status.online])
	on_idle = len([I for I in ctx.message.guild.members if I.status is discord.Status.idle])
	on_dnd = len([I for I in ctx.message.guild.members if I.status is discord.Status.dnd])
	off_line = len([I for I in ctx.message.guild.members if I.status is discord.Status.offline])
	for x in ctx.message.guild.members:
	 if x.bot == True:
	  bots += 1
	  total += 1
	 else:
	  members += 1
	  total += 1
	await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
	#await ctx.trigger_typing(ctx.message.channel)
	crea = ctx.message.guild.created_at.strftime("%A\n%-d of %B %Y\n%I:%M %p")
	emb = discord.Embed(title=":information_source: Server Information", description="Here's what I could find...", color=0xe02f5a)
	emb.set_thumbnail(url=ctx.message.guild.icon_url)
	emb.add_field(name="Name", value=ctx.message.guild.name, inline=False)
	emb.add_field(name="ID", value=ctx.message.guild.id, inline=False)
	emb.add_field(name="Region", value=ctx.message.guild.region, inline=True)
	emb.add_field(name="Varification level", value=ctx.message.guild.verification_level, inline=True)
	emb.add_field(name="Owner", value=ctx.message.guild.owner.mention, inline=False)
	emb.add_field(name="Server Status", value=f"{on}Online: {on_line}\n{ide}Idle: {on_idle}\n{dnds}Do Not Disturb: {on_dnd}\n{off}Offline: {off_line}", inline=True)
	emb.add_field(name="Server Count", value=f"{p}Members: {total}\n{p}Users: {members}\n{p}Bots: {bots}", inline=True)
	emb.add_field(name="Roles", value=len(ctx.message.guild.roles), inline=True)
	emb.add_field(name="Channels", value=str(len(ctx.message.guild.channels)), inline=True)
	emb.add_field(name="Number of Emotes", value=str(len(ctx.message.guild.emojis)), inline=False)
	emb.add_field(name="Created", value=crea, inline=True)
	emb.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url) 
	await ctx.send(embed=emb)
	
#user information
@bot.command()
async def user(ctx, member: discord.Member = None):
    if member == None:
    	member = ctx.author
    if member.status == discord.Status.online:
        member.status = f"{on}Online"
    if member.status == discord.Status.idle:
    	member.status = f"{ide}Idle"
    if member.status == discord.Status.dnd:
    	member.status = f"{dnds}Do Not Disturb"
    if member.status == discord.Status.offline:
    	member.status = f"{off}Offline"
	#def is_bot():
	#if member == is_bot:
		#char = "Bot"
	#elif: char = "User"
    await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
    #await ctx.trigger_typing(ctx.message.channel)
    char = "User"
    crea = member.created_at.strftime("%A\n%-d of %B %Y\n%I:%M %p")
    joi = member.joined_at.strftime("%A\n%-d of %B %Y\n%I:%M %p")
    emb = discord.Embed(title=f":information_source: {char} Information", description="Here's what I could find...", color=0xe02f5a)
    emb.set_thumbnail(url=member.avatar_url)
    emb.add_field(name="Name", value=member.name, inline=True)
    emb.add_field(name="ID", value=member.id, inline=True)
    emb.add_field(name="Status", value=member.status, inline=True)
    emb.add_field(name="Highest role", value=member.top_role, inline=True)
    emb.add_field(name="Created Account", value=crea, inline=True)
    emb.add_field(name="Joined Server", value=joi, inline=True)
    emb.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=emb)

#server icon picture
@bot.command()
async def icon(ctx):
	await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
	emb = discord.Embed(title="Server Icon", color=0xe02f5a)
	emb.set_image(url=ctx.message.guild.icon_url)
	await ctx.send(embed=emb)

#user avatar picture
@bot.command()
async def avatar(ctx, member:discord.User = None):
    await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
    if member == None:
        member = ctx.message.author
    emb = discord.Embed(title="User Avatar", color=0xe02f5a)
    emb.set_image(url=member.avatar_url)
    await ctx.send(embed=emb)

#bot invite
@bot.command()
async def invite(ctx):
	await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
	#await ctx.trigger_typing(ctx.message.channel)
	emb = discord.Embed(title=":envelope_with_arrow: Invite", color=0xe02f5a)
	emb.add_field(name="Link:", value="http://bit.ly/discordapp-vixen-bot")
	await ctx.send(embed=emb)

#vote for my bot
@bot.command()
async def vote(ctx):
	await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
	#await ctx.trigger_typing(ctx.message.channel)
	emb = discord.Embed(title=":arrow_up: Vote", color=0xe02f5a)
	emb.add_field(name="Link:", value="https://discordbots.org/bot/545161003617484820/vote")
	await ctx.send(embed=emb)

#generate a password
@bot.command()
async def password(ctx):
	await ctx.message.add_reaction("\N{ENVELOPE}")
	encryptkey = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',]
	encryptcode = ['1','2','3','4','5','6','7','8','9',]
	count1 = random.randint(1, 52)
	count2 = random.randint(1, 52)
	count3 = random.randint(1, 52)
	count4 = random.randint(1, 52)
	count5 = random.randint(1, 52)
	count6 = random.randint(1, 52)
	count7 = random.randint(1, 52)
	count8 = random.randint(1, 52)
	count9 = random.randint(1, 52)
	count10 = random.randint(1, 52)
	count11 = random.randint(1, 52)
	count12 = random.randint(1, 52)
	count13 = random.randint(1, 52)
	count14 = random.randint(1, 52)
	count15 = random.randint(1, 52)
	count16 = random.randint(1, 52)
	if count1 < 26:
	 key1 = (random.choice(encryptkey))
	if count1 >= 26: 
	 key1 = (random.choice(encryptcode))
	if count2 < 26:
	 key2 = (random.choice(encryptkey))
	if count2 >= 26: 
	 key2 = (random.choice(encryptcode))
	if count3 < 26:
	 key3 = (random.choice(encryptkey))
	if count3 >= 26: 
	 key3 = (random.choice(encryptcode))
	if count4 < 26:
	 key4 = (random.choice(encryptkey))
	if count4 >= 26: 
	 key4 = (random.choice(encryptcode))
	if count5 < 26:
	 key5 = (random.choice(encryptkey))
	if count5 >= 26: 
	 key5 = (random.choice(encryptcode))
	if count6 < 26:
	 key6 = (random.choice(encryptkey))
	if count6 >= 26: 
	 key6 = (random.choice(encryptcode))
	if count7 < 26:
	 key7 = (random.choice(encryptkey))
	if count7 >= 26: 
	 key7 = (random.choice(encryptcode))
	if count8 < 26:
	 key8 = (random.choice(encryptkey))
	if count8 >= 26: 
	 key8 = (random.choice(encryptcode))
	if count9 < 26: 
	 key9 = (random.choice(encryptkey))
	if count9 >= 26: 
	 key9 = (random.choice(encryptcode))
	if count10 < 26: 
	 key10 = (random.choice(encryptkey))
	if count10 >= 26: 
	 key10 = (random.choice(encryptcode))
	if count11 < 26: 
	 key11 = (random.choice(encryptkey))
	if count11 >= 26: 
	 key11 = (random.choice(encryptcode))
	if count12 < 26:
	 key12 = (random.choice(encryptkey))
	if count12 >= 26:
	 key12 = (random.choice(encryptcode))
	if count13 < 26:
	 key13 = (random.choice(encryptkey))
	if count13 >= 26:
	 key13 = (random.choice(encryptcode))
	if count14 < 26:
	 key14 = (random.choice(encryptkey))
	if count14 >= 26:
	 key14 = (random.choice(encryptcode))
	if count15 < 26:
	 key15 = (random.choice(encryptkey))
	if count15 >= 26:
	 key15 = (random.choice(encryptcode))
	if count16 < 26:
	 key16 = (random.choice(encryptkey))
	if count16 >= 26:
	 key16 = (random.choice(encryptcode))
# There are about ???,???,??? different password combinations that can be generated.
	encryptedpass = (key1 + key2 + key3 + key4 + key5 + key6 + key7 + key8 + key9 + key10 + key11 + key12 + key13 + key14 + key15 + key16)
	emb = discord.Embed(description='Here is your randomly generated password: ' + '`' + encryptedpass + '`', color=0xe02f5a)
	await ctx.author.send(embed=emb)

#counts all the servers the bot is on
@bot.command()
@commands.is_owner()
async def servercount(ctx):
	await ctx.message.add_reaction("\N{ENVELOPE}")
	emb = discord.Embed(title="Server Count", description=f"Currently watching over {str(len(bot.guilds))} Discord servers", color=0xe02f5a)
	await ctx.author.send(embed=emb)

#say command
@bot.command()
async def say(ctx, *msg):
    echo = ' '.join(msg)
    message = ctx.message
    await message.delete()
    return await ctx.send(echo)

#embed command
@bot.command()
async def embed(ctx, *msg):
    echo = ' '.join(msg)
    message = ctx.message
    await message.delete()
    emb = discord.Embed(description=echo, color=0xe02f5a)
    return await ctx.send(embed=emb)

#discord ToS command
@bot.command()
async def tos(ctx):
    emb = discord.Embed(title="Discord Terms of Service", url="https://discordapp.com/terms", description="This is the Discord ToS meta description. Wow, helpful meta description Discord. Thanks!", color=0x7289da)
    emb.set_author(name="Discord")
    emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/535747082192027651/550348313866534950/discordapp.png")
    msg = await ctx.send(embed=emb)
    await msg.add_reaction(discord.utils.get(bot.emojis, name="discord"))

#love % command
@bot.command()
async def lovecalc(ctx, member:discord.User = None):
    if member == ctx.author:
        await ctx.send("You can't calculate yourself...")
        return
    if member == None:
        await ctx.send("You can't calculate nothing...")
        return
    await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
    emb = discord.Embed(title="Love Calculator", description=f"**{ctx.message.author.name}《 :heartpulse: 》{member.name}**", color=0xe02f5a)
    emb.add_field(name="Result:", value=f"{random.choice(config.heart)}")
    emb.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url) 
    await ctx.send(embed=emb)
	
#Pay your respects command
@bot.command()
async def f(ctx, *, message = None):
    emoji = [":heart:", ":blue_heart:", ":green_heart:", ":purple_heart:", ":yellow_heart:"]
    if message == None:
        await ctx.send(f"**{ctx.author.name}** has paid their respects {random.choice(emoji)}")
    else:
        await ctx.send(f"**{ctx.author.name}** has paid their respects to **{message}** {random.choice(emoji)}")

#Poll command
@bot.command()
@commands.has_permissions(administrator = True)
async def poll(ctx, polltitle = None, *, pollmessage = None):
    if polltitle == None:
        await ctx.send(f"You must provide a title... (eg: {prefix}poll <title> <description>)")
        return
    elif pollmessage == None:
        await ctx.send(f"You must provide a description... (eg: {prefix}poll <title> <description>)")
        return
    else:
        embed = discord.Embed(title="**`P` `O` `L` `L`**", color=0x7289da,)
        embed.add_field(name=f"{polltitle}", value=f"{pollmessage}", inline=False)
        embed.add_field(name=f"Vote!", value="<:green_check_mark:553182041768853504> : `Yes`", inline=True)
        embed.add_field(name=" ‏‏‎ ", value="<:red_cross_mark:553181852228255745> : `No`", inline=True)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
        await msg.add_reaction(discord.utils.get(bot.emojis, name="red_cross_mark"))
	
#Says something mean about you. (40 insults)
@bot.command()
async def insult(ctx, member:discord.User = None):
    if member == None:
        member = ctx.message.author
    if member == id("257784039795064833"):
    	await ctx.send("You can't insult my master!")
    	return
    if member == id("545161003617484820"):
    	msg = await ctx.send(f"You can't insult me... {ctx.message.author.name} {random.choice(config.insult)}")
    	await msg.add_reaction(discord.utils.get(bot.emojis, name="OkayChamp"))
    	return
    else:
    	msg = await ctx.send(f"{member.name} {random.choice(config.insult)}")  # Mention the user and say the insult
    	await msg.add_reaction(discord.utils.get(bot.emojis, name="OkayChamp"))
    	return

#Says something funny to you. (35 jokes)
@bot.command()
async def joke(ctx, member:discord.User = None):
    if member == None:
        member = ctx.message.author
    if member == id("257784039795064833"):
    	await ctx.send("You can't insult my master!")
    	return
    if member == id("545161003617484820"):
    	msg = await ctx.send(f"You can't insult me... {ctx.message.author.name} {random.choice(config.jokes)}")
    	await msg.add_reaction(discord.utils.get(bot.emojis, name="OkayChamp"))
    	return
    else:
    	msg = await ctx.send(f"{member.name} {random.choice(config.jokes)}")  # Mention the user and say the insult
    	await msg.add_reaction(discord.utils.get(bot.emojis, name="OkayChamp"))
    	return

#urban command
@bot.command()
@commands.is_nsfw()
async def urban(ctx, *msg):
    #Searches on the Urban Dictionary.
    try:
        word = ' '.join(msg)
        api = "http://api.urbandictionary.com/v0/define"
        # Send request to the Urban Dictionary API and grab info
        response = requests.get(api, params=[("term", word)]).json()
        emb = discord.Embed(description="No results found...", colour=0xe02f5a)
        if len(response["list"]) == None:
            return await ctx.send(embed=emb)
        ter = response['list'][0]["word"]
        auth = response['list'][0]["author"]
        defin = response['list'][0]["definition"]
        examp = response['list'][0]["example"]
        upvotes = (response['list'][0]["thumbs_up"])
        dwnvotes = (response['list'][0]["thumbs_down"])
        # Add results to the embed
        emb = discord.Embed(title=f"www.urbandictionary.com/{ter}", url=f"https://www.urbandictionary.com/define.php?term={word}", description=f'**"{ter}"**\n*by {auth}*', colour=0xe02f5a)
        emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/535747082192027651/548848910848753684/urbandictionary.png")
        emb.set_author(name=f"Word:")
        emb.add_field(name="Definition:", value=defin, inline=False)
        emb.add_field(name="Examples:", value=examp, inline=False)
        emb.add_field(name="Votes:", value=f":thumbsup: {upvotes} | :thumbsdown: {dwnvotes}", inline=True)
        await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
        await ctx.send(embed=emb)
    except:
        await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="red_cross_mark"))
        emb = discord.Embed(title="`Error`", description="404: Not Found... <:blobsweat:546851214026080307>", colour=0xe02f5a)
        await ctx.send(embed=emb)
		#\nuhhhh... I don't know how to get those... <:blobsweat:546851214026080307>

#birthday countdown!
@bot.command()
async def birthday(ctx):
    await ctx.send("**" + str(diff.days) + "**" + " day(s) left until my Birthday! :gift_heart:")  # Convert the 'diff' integer into a string and say the message

#hug command (15 gifs)
@bot.command()
async def hug(ctx, member:discord.User = None):
	if member == ctx.author:
	    await ctx.send("You can't hug yourself...")
	    return
	if member == None:
		await ctx.send("You can't hug thin air...")
		return
	emb = discord.Embed(description=f"***{member.name}**, you got a hug from **{ctx.message.author.name}***", color=0xe02f5a)
	emb.set_image(url=random.choice(config.hug))
	await ctx.send(embed=emb)
    #await msg.add_reaction(discord.utils.get(bot.emojis, name="OkayChamp"))

#kiss command (15 gifs)
@bot.command()
async def kiss(ctx, member:discord.User = None):
	if member == ctx.author:
		await ctx.send("You can't kiss yourself...")
		return
	if member == None:
		await ctx.send("You can't kiss thin air...")
		return
	emb = discord.Embed(description=f"***{member.name}**, you got a kiss from **{ctx.message.author.name}***", color=0xe02f5a)
	emb.set_image(url=random.choice(config.kiss))
	await ctx.send(embed=emb)

#pat command (15 gifs)
@bot.command()
async def pat(ctx, member:discord.User = None):
	if member == ctx.author:
		await ctx.send("You can't pat yourself...")
		return
	if member == None:
		await ctx.send("You can't pat thin air...")
		return
	emb = discord.Embed(description=f"***{member.name}**, you got a pat from **{ctx.message.author.name}***", color=0xe02f5a)
	emb.set_image(url=random.choice(config.pat))
	await ctx.send(embed=emb)
	
#slap command (15 gifs)
@bot.command()
async def slap(ctx, member:discord.User = None):
	if member == ctx.author:
		await ctx.send("You can't slap yourself...")
		return
	if member == None:
		await ctx.send("You can't slap thin air...")
		return
	emb = discord.Embed(description=f"***{member.name}**, you got a slap from **{ctx.message.author.name}***", color=0xe02f5a)
	emb.set_image(url=random.choice(config.slap))
	await ctx.send(embed=emb)

#help command
@bot.command()
async def help1(ctx):
	emb = discord.Embed(title="📑 **Commands**", description='here are all my commands...', color=0xe02f5a)
	emb.add_field(name="👑 Aministrative commands", value=f"{p}ban\n{p}kick\n{p}purge\n{p}clear\n{p}delete\n{p}clean\n{p}ping\n{p}count", inline=False)
	emb.add_field(name="🎀 General commands", value=f"{p}server\n{p}user\n{p}tos\n{p}say\n{p}embed\n{p}avatar\n{p}icon\n{p}password\n{p}invite\n{p}vote", inline=False)
	emb.add_field(name="✨ Fun Commands", value=f"{p}hug\n{p}kiss\n{p}pat\n{p}slap\n{p}birthday\n{p}urban\n{p}joke\n{p}insult", inline=False)
	emb.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
	await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
	await ctx.send(embed=emb)
	
#help command
@bot.command()
async def help(ctx):
	emb = discord.Embed(title="📑 **Commands**", description='here are all my commands...', color=0xe02f5a)
	emb.add_field(name="👑 Aministrative commands", value="`ban`, `kick`, `poll`, `purge`, `clear`, `delete`, `clean`, `ping`, `count`", inline=False)
	emb.add_field(name="🎀 General commands", value="`server`, `user`, `tos`, `say`, `embed`, `avatar`, `icon`, `password`, `invite`, `vote`", inline=False)
	emb.add_field(name="✨ Fun Commands", value="`hug`, `kiss`, `pat`, `slap`, `lovecalc`, `f`, `birthday`, `urban`, `joke`, `insult`", inline=False)
	emb.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
	await ctx.message.add_reaction(discord.utils.get(bot.emojis, name="green_check_mark"))
	await ctx.send(embed=emb)

bot.run(os.getenv("TOKEN"))
