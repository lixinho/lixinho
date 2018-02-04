import discord, random, requests, bs4, json
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

@bot.command(pass_context=True)
async def printEmbed(context, *params):
	paramList = [param.lower() for param in list(params)]
	cryptoList = []

	for crypto in paramList:
		res = requests.get('https://api.coinmarketcap.com/v1/ticker/' + crypto + '/?convert=BRL')
		try:
			res.raise_for_status()
		except Exception as e:
			print(str(e))
			continue

		coinMarketCap = json.loads(res.text)
		cryptoList.append(coinMarketCap[0])

	print(cryptoList)

# Reads the variable set in Heroku.
bot.run(os.environ.get('TOKEN', None))