# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import discord
import os
import random
from discord.ext import commands
from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return "Bot is online"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


#TODO put these lists into a 2d array
#TODO clean the code
normal = []
offensive = []
valorant = []
intents = discord.Intents.all()
client = commands.Bot(command_prefix='$', intents=intents)


def writeToList(fileName, listName):
    f = open(fileName, "r")
    for line in f:
        listName.append(line.rstrip())


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('with her sanity'))
    await client.tree.sync()
    #TODO automate this with a list
    #TODO add more categories and lines
    writeToList("normal.txt", normal)
    writeToList("offensive.txt", offensive)
    writeToList("valorant.txt", valorant)
    print('Initilization done.')


@client.command()
async def generate(ctx, category='normal'):
    embed = discord.Embed(title="Rizz Line Generator", color=0xC331FF)
    #TODO replace the if statements with switch case style or use try with index
    #TODO add slash command for it, allows for multiple selection
    rizzLine = ''
    if category == 'normal':
        rizzLine = random.choice(normal)
    elif category == 'offensive':
        rizzLine = random.choice(offensive)
    elif category == 'valorant':
        rizzLine = random.choice(valorant)
    elif category == 'all':
        rizzLine = random.choice(normal + offensive + valorant)
    else:
        rizzLine = "Please enter a valid category"
    embed.add_field(name='Generated Rizz Line', value=rizzLine)
    embed.set_footer(text=f'Requested by {ctx.message.author}',
                     icon_url=ctx.message.author.display_avatar)
    await ctx.send(embed=embed)


@client.command()
async def feedback(ctx):
    await ctx.send(
        'Contact xPugno#3468 or visit the discord in $info for feedback, suggesting more rizz lines, and other info'
    )


@client.command()
async def updates(ctx):
    await ctx.send(
        'Alpha Expected July 4: Includes\n - functional $help command\n - more rizz lines\n - cleaner looking embeds\n - slash commands'
    )


@client.command()
async def info(ctx):
    embed = discord.Embed(title="Bot Info", color=0xFFD431)
    embed.add_field(
        name="Description",
        value=
        'VERSION: PRE-ALPHA\n\nwill help you rizz people up\n\n$help for some help',
        inline=True)
    embed.add_field(
        name="Invite Link",
        value=
        'https://discord.com/api/oauth2/authorize?client_id=1101264563749535854&permissions=2147551232&scope=applications.commands%20bot',
        inline=False)
    embed.add_field(name="Official Bot Discord Server",
                    value="https://discord.gg/eAZ9WtuTpz")
    embed.set_footer(text=f'Requested by {ctx.message.author}',
                     icon_url=ctx.message.author.display_avatar)
    await ctx.send(embed=embed)


@client.tree.command(name="ping", description="get the latency")
async def ping(interaction):
    await interaction.response.send_message(f"Ping: {client.latency*1000}ms")


@client.command()
async def sync(ctx):
    print("sync command")
    if ctx.author.id == 567924760370085899:
        await client.tree.sync()
        await ctx.send('Command tree synced.')


try:
    keep_alive()
    client.run(os.getenv("TOKEN"))
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
