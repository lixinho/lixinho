import discord, random, requests, bs4, json, os, re
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

# Crypto Stuff
@bot.command(pass_context=True)
async def crypto(context, *params):
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

	cryptoList = sorted(cryptoList, key=lambda k: int(k['rank']))
	embed = discord.Embed(title='Cryptocurrency Market Capitalizations', url='https://coinmarketcap.com/', color=discord.Color.gold())
	for cryptoDict in cryptoList:
		embed.add_field(
			name='[{}º] {} (*{}*)'.format(
				cryptoDict['rank'],
				cryptoDict['name'],
				cryptoDict['symbol']),
			value='**Price (USD)**: {}\n**Price (BRL)**: {}\n**Price (BTC)**: {}\n**% Change (24h)**: {}\n**% Change (7d)**: {}\n'.format(
				cryptoDict['price_usd'],
				cryptoDict['price_brl'],
				cryptoDict['price_btc'],
				cryptoDict['percent_change_24h'],
				cryptoDict['percent_change_7d']),
			inline=False)

	await bot.say(embed=embed)

# Util Stuff
@bot.command(pass_context=True)
async def blacklist(context, *channels : discord.Channel):
	blacklistFile = open('blacklist.txt', 'r')
	print(blacklistFile.read())
	blacklistFile.close()
		

# Reads the variable set in Heroku.
bot.run(os.environ.get('TOKEN', None))