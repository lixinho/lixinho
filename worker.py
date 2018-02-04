import discord, requests, json, bs4, os
from discord.ext import commands
import random

roles_list = ["Top", "Jungle", "Mid", "AD-Carry", "Support"]
champions_list = ["Aatrox", "Ahri", "Akali", "Alistar", "Amumu", "Anivia", "Annie", "Ashe", "Aurelion Sol", "Azir", "Bardo", "Blitzcrank", "Brand", "Braum", "Caitlyn", "Camille", "Cassiopeia", "Cho'Gath", "Corki", "Darius", "Diana", "Dr. Mundo", "Draven", "Ekko", "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", "Gangplank", "Garen", "Gnar", "Gragas", "Graves", "Hecarim", "Heimerdinger", "Illaoi", "Irelia", "Ivern", "Janna", "Jarvan IV", "Jax", "Jayce", "Jhin", "Jinx", "Kalista", "Karma", "Karthus", "Kassadin", "Katarina", "Kayle", "Kayn", "Kennen", "Kha'Zix", "Kindred", "Kled", "Kog'Maw", "LeBlanc", "Lee Sin", "Leona", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai", "Master Yi", "Miss Fortune", "Mordekaiser", "Morgana", "Nami", "Nasus", "Nautilus", "Nidalee", "Nocturne", "Nunu", "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Quinn", "Rakan", "Rammus", "Rek'Sai", "Renekton", "Rengar", "Riven", "Rumble", "Ryze", "Sejuani", "Shaco", "Shen", "Shyvana", "Singed", "Sion", "Sivir", "Skarner", "Sona", "Soraka", "Swain", "Syndra", "Tahm Kench", "Taliyah", "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere", "Twisted Fate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vi", "Viktor", "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah", "Xerath", "Xin Zhao", "Yasuo", "Yorick", "Zac", "Zed", "Ziggs", "Zilean", "Zoe", "Zyra"]
words_list = ["perder", "trollar", "ser carregado", "afundar", "mostrar o que sabe"]

description = 'The sad bot.'

bot = commands.Bot(command_prefix='@', description=description)

@bot.event
async def on_ready():
    print('-' * 25)
    print('Logged in as:')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('-' * 25)

@bot.command(pass_context=True)
async def lChampion(context):
    randomChampion = champions_list[random.randint(1, len(champions_list) - 1)]
    await bot.say('**{}** deveria {} jogando de **{}**!'.format(
        context.message.author.nick, 
        words_list[random.randint(1, len(words_list) - 1)], 
        champions_list[random.randint(1, len(champions_list) - 1)]))

@bot.command(pass_context=True)
async def lRoles(context):
    available_roles = list(roles_list)

    primaryRole = available_roles[random.randint(1, len(available_roles) - 1)]
    available_roles.remove(primaryRole)
    secondaryRole = available_roles[random.randint(1, len(available_roles) - 1)]

    await bot.say('Se é pra {}, **{}** deveria colocar de primária **{}** e de secundária **{}**!'.format(
        words_list[random.randint(1, len(words_list) - 1)], 
        context.message.author.nick,
        primaryRole,
        secondaryRole))

@bot.command()
async def lRand(start : int, end : int):
    await bot.say('Eu escolho: **' + str(random.randint(start, end)) + '**!')

@bot.command()
async def lChoose(*opt):
    options = list(opt)
    await bot.say('Eu escolho: **' + str(options[random.randint(0, len(options) - 1)]) + '**!')

@bot.command(pass_context=True)
async def lCrypto(context, *opt):
    cryptoList = [crypto.lower() for crypto in list(opt)]

    allOutputs = ''
    for crypto in cryptoList:
        res = requests.get('https://api.coinmarketcap.com/v1/ticker/' + crypto + '/?convert=BRL')
        try:
            res.raise_for_status()
        except Exception as e:
            print(str(e))
            continue

        coinMarketCap = json.loads(res.text)

        output = '**[{}º]** {} (*{}*):\n'.format(coinMarketCap[0]['rank'], coinMarketCap[0]['name'], coinMarketCap[0]['symbol'])
        output += '\t**Preço (USD):** {}\n'.format(coinMarketCap[0]['price_usd'])
        output += '\t**Preço (BRL):** {}\n'.format(coinMarketCap[0]['price_brl'])
        output += '\t**Preço (BTC):** {}\n'.format(coinMarketCap[0]['price_btc'])
        output += '\t**Mudança (24h):** {}%\n'.format(coinMarketCap[0]['percent_change_24h'])
        output += '\t**Mudança (7d):** {}%\n\n'.format(coinMarketCap[0]['percent_change_7d'])
        allOutputs += output

    await bot.send_message(context.message.channel, embed=discord.Embed(color=discord.Color.gold(), description=allOutputs))

@bot.command()
async def lWord(amount : int):
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

    await bot.say('Eu escolho: **' + ' '.join(wordList) + '**!')

@bot.command(pass_context=True)
async def lClear(context, amount : int):
    if context.message.channel.id != '409522008016289793':
        await bot.send_message(context.message.channel, embed=discord.Embed(color=discord.Color.red(), description='**VAI APAGAR NOSSA HISTÓRIA NÃO PORRA**'))
        return

    messages = []
    async for message in bot.logs_from(context.message.channel, limit=amount):
         messages.append(message)

    await bot.delete_messages(messages)

bot.run(os.environ.get('TOKEN', None))