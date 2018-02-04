import discord, random, requests, bs4, json, os
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

	cryptoList = sorted(cryptoList, key=lambda k: k['rank'])
	print(cryptoList)
	cryptoRank = ''
	cryptoName = ''
	cryptoSymbol = ''
	cryptoUSD = ''
	cryptoBRL = ''
	cryptoBTC = ''
	crypto24h = ''
	crypto7d = ''

	for crypto in cryptoList:
		cryptoRank += crypto['rank'] + '\n'
		cryptoName += crypto['name'] + '\n'
		cryptoSymbol += crypto['symbol'] + '\n'
		cryptoUSD += crypto['price_usd'] + '\n'
		cryptoBRL += crypto['price_brl'] + '\n'
		cryptoBTC += crypto['price_btc'] + '\n'
		crypto24h += crypto['percent_change_24h'] + '\n'
		crypto7d += crypto['percent_change_7d'] + '\n'

	embed = discord.Embed(title='Cryptocurrencies Informations', color=discord.Color.gold())
	embed.add_field(name='Rank', value=cryptoRank, inline=True)
	embed.add_field(name='Name', value=cryptoName, inline=True)
	embed.add_field(name='Symbol', value=cryptoSymbol, inline=True)
	embed.add_field(name='USD', value=cryptoUSD, inline=True)
	embed.add_field(name='BRL', value=cryptoBRL, inline=True)
	embed.add_field(name='BTC', value=cryptoBTC, inline=True)
	embed.add_field(name='24h (%)', value=crypto24h, inline=True)
	embed.add_field(name='7d (%)', value=crypto7d, inline=True)

	await bot.say(embed=embed)

# Reads the variable set in Heroku.
bot.run(os.environ.get('TOKEN', None))