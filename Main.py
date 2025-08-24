import random
import webserver
import json
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

def save_stats(stats_data):
    with open('user_stats.json', 'w') as f:
        json.dump(stats_data, f, indent=4)

def load_stats():
    try:
        with open('user_stats.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
def load_Week():
    try:
        with open('Weeklies.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}



bot = commands.Bot(command_prefix='!', intents=intents)



@bot.event
async def on_ready():
    print(f"we are ready to go in, {bot.user.name}")


@bot.command()
async def weekly(ctx):
    Weekly = load_Week()
    await ctx.send(f"Here are this weeks modifiers!")
    for i in range(3):
        count = i + 1
        random_integer = random.randint(1, 43)
        rand_str = str(random_integer)
        await ctx.send(f"#{count}: {Weekly[rand_str]} \n")
        print("working")

#Code for !hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")

#Code for !checkin
@bot.command()
async def checkin(ctx, arg1, arg2, arg3):
    user_stats = load_stats()
    try:
        with open("EffortLog.txt", "a") as f:
            f.write(f"{ctx.author}: {arg1}, {arg2}, {arg3}\n")
        await ctx.send(f"{ctx.author}, good job! another day has been logged")
    except Exception as e:
        await ctx.send(f"and error occurred while logging: {e}")

    #sets the user ID and Log Count
    user_id = str(ctx.author)
    if user_id not in user_stats:
        user_stats[user_id] = {"Days logged": 0, "Time logged": 0, "Last Logged": 0}
        print("functional")
    #tracks time
    date_check = str(user_stats[user_id]["Last Logged"])
    if arg1 != date_check:
        user_stats[user_id]["Last Logged"] = arg1
        user_stats[user_id]["Days logged"] += 1
    time_add = int(arg2)
    user_stats[user_id]["Time logged"] += time_add
    save_stats(user_stats)

#code for !days
@bot.command()
async def days(ctx):
    user_stats = load_stats()
    user_id = str(ctx.author)
    await ctx.send(f"you have logged: {user_stats[user_id]['Days logged']} days")

#code for !lastlog
@bot.command()
async def lastlog(ctx):
    user_stats = load_stats()
    user_id = str(ctx.author)
    await ctx.send(f"you last logged: {user_stats[user_id]['Last Logged']}")

#code for !time
@bot.command()
async def time(ctx):
    user_stats = load_stats()
    user_id = str(ctx.author)
    await ctx.send(f"you last logged: {user_stats[user_id]['Time Logged']}")

#code for !help
@bot.command()
async def info(ctx):
    with open('help.txt', 'r') as f:
        content = "\n".join(f.readlines())
    await ctx.send(content)

webserver.keep_alive()
bot.run(token, log_handler= handler, log_level=logging.DEBUG)