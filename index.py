import discord

from discord.ext import commands

import requests

import json

import random

bot = commands.Bot(command_prefix='-', description='Rule Book\'s '
    + 'playground bot')

@bot.command(name='abbamembers', aliases=['abbamember'],
    help='List of Abba members')
async def _abbamember(ctx):
    members = "'Agnetha Fältskog', 'Anni-Frid \"Frida\" Lyngstad',"
        + "'Björn Ulvaeus', 'Benny Andersson'"
    teal = discord.Colour.dark_teal()
    embed = discord.Embed(title='Members List', colour=teal,
        description=members)
    embed.set_footer(text='These are the four main members of *Abba*')

    print(embed.to_dict())
    await ctx.send(embed=embed)

@bot.command(name='abba', help='Random top 10 Abba song')
async def _abba(ctx):
    array = ['https://www.youtube.com/watch?v=xFrGuyw1V8s',
    'https://www.youtube.com/watch?v=unfzfe8f9NI',
    'https://www.youtube.com/watch?v=XEjLoHdbVeE',
    'https://www.youtube.com/watch?v=p4QqMKe3rwY',
    'https://www.youtube.com/watch?v=-crgQGdpZR0',
    'https://www.youtube.com/watch?v=92cwKCU8Z5c',
    'https://www.youtube.com/watch?v=cvChjHcABPA',
    'https://www.youtube.com/watch?v=iUrzicaiRLU',
    'https://www.youtube.com/watch?v=iUrzicaiRLU',
    'https://youtu.be/WkL7Fkigfn8',
    'https://youtu.be/dQsjAbZDx-4',
    'https://youtu.be/za05HBtGsgU',
    'https://www.youtube.com/watch?v=BshxCIjNEjY',
    'https://youtu.be/iJ90ZqH0PWI',
    'https://www.youtube.com/watch?v=2seCB54Bv-c',
    'https://www.youtube.com/watch?v=ETxmCCsMoD0',
    'https://www.youtube.com/watch?v=IIKAe8Wi0S0',
    'https://www.youtube.com/watch?v=dDI7x1nwTUw',
    'https://youtu.be/tW3HN_pvbE4',
    'https://youtu.be/mhr6tUE32YA']
    n = random.randint(0,10)
    print(n)
    await ctx.send('Abba\'s biggest hits #' + str(n) + ': ' + array[n])

@bot.command(name='runes', help='Shows runes from latest draft/ranked match')
async def _runes(ctx):
    region = 'na1'
    region_v5 = 'americas' # americas, asia, europe
    summoner_name = "summoner name"
    if len(ctx.message.split()) > 1:
        sum_name_array = [i for i in ctx.message.split()[1:]]
        summoner_name = ''
        for i in sum_name_array:
            summoner_name = summoner_name + i
    summoner_name.replace(' ', '%20')

    discord_bot_token_id = '..'
    dragontail_filepath = '..' # 'C:/Users/trunk/Documents/Discord Bots/Takoyaki'
    API_KEY = '..' # riot games api key
    BASE_RIOTAPI_CALL = 'https://{region}.api.riotgames.com'
    SUMMONER_V4_QUERY = '/lol/summoner/v4/summoners/by-name/{name}' + API_KEY
    MATCH_IDS_V5_QUERY = '/lol/match/v5/matches/by-puuid/{puuid}/ids'
        + API_KEY
    MATCH_V5_QUERY = '/lol/match/v5/matches/{matchId}' + API_KEY

    x = requests.get(BASE_RIOTAPI_CALL.format(region=region)
    	+ SUMMONER_V4_QUERY.format(name=summoner_name))

    print(x.status_code)

    puuid = x.json()['puuid']
    y = requests.get(BASE_RIOTAPI_CALL.format(region=region_v5)
    	+ MATCH_IDS_V5_QUERY.format(puuid=puuid)) # list of 20 match numbers

    latest_match = y.json()[0]
    z = requests.get(BASE_RIOTAPI_CALL.format(region=region_v5)
    	+ MATCH_V5_QUERY.format(matchId=latest_match))

    player_index_in_match = 0
    for index, player_uid in enumerate(z.json()['metadata']['participants']):
    	if player_uid == puuid:
    		player_index_in_match = index

    match = z.json()['info']
    player_data = match['participants'][player_index_in_match]
    perk_data = player_data['perks']['styles']

    style_ids = []
    perk_ids = []
    for i, v in enumerate(perk_data):
    	perk_ids.append([j['perk'] for j in perk_data[i]['selections']])
    	style_ids.append(v['style'])

    runes_reforged = open(dragontail_filepath
        + '/dragontail-11.8.1/11.8.1/data/en_US/runesReforged.json',)
    runes_mapping = json.load(runes_reforged)

    ic_pf = "http://ddragon.leagueoflegends.com/cdn/img/"
    file_pf = dragontail_filepath
        + '/dragontail-11.8.1/img/'

    RUNE_TREES = []
    fileList = []
    for i in runes_mapping:
    	if i['id'] in style_ids:
    		RUNE_TREES.append(i['key'])
    		fileList.append(discord.File(file_pf + i['icon']))
    		for j in i['slots']:
    			for k in j['runes']:
    				if k['id'] in perk_ids[0]:
    					RUNE_TREES.append(k['key'])
    					fileList.append(discord.File(file_pf + k['icon']))
    				elif k['id'] in perk_ids[1]:
    					RUNE_TREES.append(k['key'])
    					fileList.append(discord.File(file_pf + k['icon']))

    await ctx.send('Runes for ' + summoner_name + '\'s latest match: ' + RUNE_TREES, files=fileList)

bot.run(discord_bot_token_id) # discord bot token id