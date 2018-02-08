import discord, random, requests, bs4, json, os, re, asyncio
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

	if len(cryptoList) == 0:
		return

	cryptoList = sorted(cryptoList, key=lambda k: int(k['rank']))
	embed = discord.Embed(title='Cryptocurrency Market Capitalizations', url='https://coinmarketcap.com/', color=discord.Color.green())
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
async def survey (context, question, *reactions):
	surveyAuthor = context.message.author

	tmpMessage = await bot.send_message(context.message.channel, question)
	for reaction in reactions:
		await bot.add_reaction(tmpMessage, reaction)

	botMessage = discord.utils.get(bot.messages, id=tmpMessage.id)
	authorMessage = await bot.wait_for_message(channel=context.message.channel, author=surveyAuthor, content='$survey')
	await bot.say(embed=discord.Embed(color=discord.Color.green(), description='**{}** ended the survey!'.format(surveyAuthor.nick)))

	pmMessage = 'Here are the results of your survey!\n'
	for reaction in botMessage.reactions:
		reactors = await bot.get_reaction_users(reaction)
		reactors = [reactor for reactor in reactors if reactor.id != bot.user.id]
		pmMessage += 'Users who reacted with {} (Total: {}):\n'.format(reaction.emoji, len(reactors))
		for reactor in reactors:
			pmMessage += '\t- {};\n'.format(reactor.name)

	await bot.send_message(surveyAuthor, content=pmMessage)


@bot.command()
async def rand(start : int, end : int):
	await bot.say(embed=discord.Embed(color=discord.Color.green(), description='Here\'s what I\'ve chosen: **' + str(random.randint(start, end)) + '**!'))

@bot.command()
async def choose(*opt):
	options = list(opt)
	await bot.say(embed=discord.Embed(color=discord.Color.green(), description='Here\'s what I\'ve chosen: **' + str(random.choice(options)) + '**!'))

@bot.command(pass_context=True)
async def clear(context, amount : int):
	whitelistFile = open('whitelist.txt')

	channelRegex = re.compile(r'%s' % context.message.channel.id)
	mo = channelRegex.search(whitelistFile.read())

	if mo == None:
		msg = await bot.say(embed=discord.Embed(color=discord.Color.red(), description='You can\'t use this command here. (Channel blacklisted)'))
		await asyncio.sleep(3)
		await bot.delete_messages([msg, context.message])
	else:
		messages = []
		async for message in bot.logs_from(context.message.channel, limit=amount):
			messages.append(message)
		await bot.delete_messages(messages)

	whitelistFile.close()

@bot.command()
async def word(amount : int):
	wordList = []
	wordUrl = 'https://www.palavrasque.com/palavra-aleatoria.php?Submit=Nova+palavra'

	for i in range(amount):
		res = requests.get(wordUrl)
		res.encoding = 'utf-8'
		try:
			res.raise_for_status()
		except Exception as e:
			print(str(e))
			continue

		soup = bs4.BeautifulSoup(res.text, 'html.parser')
		word = soup.select('b')[0].getText()
		wordList.append(word)

	await bot.say(embed=discord.Embed(color=discord.Color.green(), description='Here are your random words: **' + ' '.join(wordList) + '**!'))

# Help Stuff
@bot.command()
async def commands():
	embed = discord.Embed(color=discord.Color.green(), title='My Commands', description='<:lixinho_trab:409793689809059841> Here\'s my commands list:')
	embed.add_field(name='?choose <opt #1> ... <opt #2>', value='<:lixinho:409778817264254989> Chooses a random element from the specified options.', inline=False)
	embed.add_field(name='?clear <n>', value='<:lixinho:409778817264254989> Deletes "n" messages in the chat room.', inline=False)
	embed.add_field(name='?crypto <crypto #1> ... <crypto #n>', value='<:lixinho:409778817264254989> Searches for informations regarding the specified cryptocurrencies.', inline=False)
	embed.add_field(name='?rand <num #1> <num #2>', value='<:lixinho:409778817264254989> Generates a random number "n" such as `num #1 <= n <= num #2`.', inline=False)
	embed.add_field(name='?survey "text" <emoji #1> ... <emoji #n>', value='<:lixinho:409778817264254989> Creates a survey with the specified emojis. Use `$survey` to end the survey and receive the results.', inline=False)
	embed.add_field(name='?word <n>', value='<:lixinho:409778817264254989> Generates "n" random words.', inline=False)
	await bot.say(embed=embed)

# Reads the variable set in Heroku.
bot.run('NDA4NDU5NjA4NDYyNzIxMDI0.DVQXww.-lcXjbzC6CwQw014gSrVPM88hWY')
#bot.run(os.environ.get('TOKEN', None))