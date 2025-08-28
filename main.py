import asyncio
import pickle
import discord
from discord import client
from discord.ext import commands
from pytz import timezone
import datetime
import zoomdis
import classSchedule
from classSchedule import CClass
import os, dotenv

dotenv.load_dotenv()
UTC = timezone("Asia/Dhaka")

intents = discord.Intents().all()
client = commands.Bot(command_prefix = '-', intents=intents)

async def dm_function(content):
    for s in students:
        await s.send(embed=content)

@client.event
async def on_ready():
    print('Apple landed on head!')
    #global variabls 
    global pho
    pho = client.get_guild(os.getenv("PHO_GUILD_ID"))
    global phoGeneralText
    phoGeneralText =await client.fetch_channel(os.getenv("PHO_GENERAL_TEXT_ID"))
    global phoGeneralVoice
    phoGeneralVoice = await client.fetch_channel(os.getenv("PHO_GENERAL_VOICE_ID"))
    global askm
    askm = await pho.fetch_member(os.getenv("ASKM_USER_ID"))
    global hackermub
    hackermub = await pho.fetch_member(os.getenv("HACKERMUB_USER_ID"))
    global students
    students = await pho.fetch_members().flatten()
    students.remove(askm)
    # students.remove(hackermub)
    students.remove(client.user)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Make sure you put the required arguments.')

@client.command()
async def hello(ctx):
    await ctx.message.add_reaction('\U0001F34E')
    await ctx.send(ctx.author.mention+' hello')

@client.command()
async def create(ctx):
    if ctx.author == askm or ctx.author == hackermub:
        y = zoomdis.createMeeting()
        join_URL = y["join_url"]
        meetingPassword = y["password"]
        topic = y["topic"]
        embed = discord.Embed(title = topic, color = 0x39b0fa)
        embed.set_thumbnail(url = pho.icon_url)
        embed.add_field(name="JoinURL",value=join_URL,inline=False)
        embed.add_field(name="Password",value=meetingPassword,inline=False)
        await ctx.message.add_reaction('\U0001F34E')
        await ctx.send(content="@everyone",embed=embed)
        await dm_function(embed)
    else:
        await ctx.message.add_reaction(u"\u26D4")
        await ctx.send('nice try hehe')

@client.command()
async def dm(ctx,*,msg:str):
    await ctx.message.add_reaction('\U0001F34E')
    await dm_function(msg)

@client.command()
async def schedule(ctx):
    await ctx.message.add_reaction('\U0001F34E')
    embed = discord.Embed(title = "Class Schedule", description = "Weekday : UTC+6 in 24 Hour Format" , color = 0x39b0fa)
    embed.set_thumbnail(url = pho.icon_url)
    for Class in classSchedule.classes:
        id = str(classSchedule.classes.index(Class)+1)
        embed.add_field(name=id+'. '+Class.weekDay,value=" at "+Class.classTime,inline=True)
    if not classSchedule.classes:
        embed.description="No class available!"
    await ctx.send(ctx.author.mention,embed=embed)

@client.command()
async def add(ctx,weekDay,classTime):
    if ctx.author==askm or ctx.author==hackermub:
        await ctx.message.add_reaction('\U0001F34E')
        res = classSchedule.classAdd(weekDay,classTime)
        await ctx.send(ctx.author.mention+res)
        pickle.dump(classSchedule.classes,open("classes.dat","wb"))
    else:
        await ctx.message.add_reaction(u"\u26D4")
        await ctx.send('nice try hehe')

@client.command()
async def remove(ctx,index:int):
    if ctx.author==askm or ctx.author==hackermub:
        await ctx.message.add_reaction('\U0001F34E')
        res = classSchedule.classRemove(index)
        print(res)
        await ctx.send(ctx.author.mention+res)
        pickle.dump(classSchedule.classes,open("classes.dat","wb"))
    else:
        await ctx.message.add_reaction(u"\u26D4")
        await ctx.send('nice try hehe')


async def classReminder():
    await client.wait_until_ready()
    while True:
        now = datetime.datetime.now(UTC)
        weekDay = now.strftime("%A")
        classTime = now.strftime("%H:%M")
        
        for Class in classSchedule.classes:
            stime=1
            if Class.weekDay == weekDay and Class.classTime == classTime:
                content = "get ready for class"
                allowed_mentions = discord.AllowedMentions(everyone = True)
                msg = await phoGeneralText.send(content = "@everyone get ready for class!", allowed_mentions = allowed_mentions)
                await dm_function(content)
                print("Alarm ",Class)
                stime = 60
            else:
                stime = 1
            await asyncio.sleep(stime)
        if not classSchedule.classes:
            await asyncio.sleep(1)

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_BOT_TOKEN") 
    classSchedule.loadClasses()
    client.loop.create_task(classReminder())
    # app.run(host='0.0.0.0', port=6969)
    client.run(TOKEN)

