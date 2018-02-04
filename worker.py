import discord, random, requests, bs4, os
from discord.ext import commands

description = 'A sad bot.'
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('-' * 15)
    print('Logged in as:')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('-' * 15)

@bot.command()
async def printEmbed():
    embed = discord.Embed()
    embed.title = 'A Title'
    embed.description = 'Luls'
    embed.add_field(name='Field #1', value='Simple', inline=True)
    embed.add_field(name='Field #2', value='Text', inline=True)
    await bot.say(embed=embed)

# Reads the variable set in Heroku.
bot.run(os.environ.get('TOKEN', None))