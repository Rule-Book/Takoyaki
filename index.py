import discord # pip install discord
from discord.ext import commands
import requests # pip install requests
import json
import random
import token_file # local file to store secrets

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

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content[:6] == '_runes':

            region_v5 = ''
            regions = ['americas', 'asia', 'esports', 'europe']
            params = message.content.split('"')
            if len(params) <= 1:
                await message.channel.send('format = \'_runes "gamename#tagname"\' region\nex: `_runes "Lee Sin#NA1" americas`')
                return
            elif len(params) >= 3 and params[2].strip() != '':
                region_input = params[2].strip()
                if region_input.lower() not in regions:
                    await message.channel.send('region *' + region_input + '* must instead be americas, asia, esports, or europe')
                    return
                else:
                    region_v5 = region_input
            else:
                region_v5 = 'americas'

            summoner_name = params[1]
            gamename = summoner_name.split('#')[0]
            tagline = summoner_name.split('#')[1]
            dragontail_filepath = 'C:/workspace/gitHome/Takoyaki' # 'C:/workspace/gitHome/Takoyaki'
            API_KEY = '/?api_key=' + token_file.api_key # riot games api key
            BASE_RIOTAPI_CALL = 'https://{region_v5}.api.riotgames.com'
            # SUMMONER_V4_QUERY = '/lol/summoner/v4/summoners/by-name/{name}' + API_KEY
            ACCOUNT_V1_QUERY = '/riot/account/v1/accounts/by-riot-id/{gamename}/{tagline}' + API_KEY
            MATCH_IDS_V5_QUERY = ('/lol/match/v5/matches/by-puuid/{puuid}/ids'
            + API_KEY)
            MATCH_V5_QUERY = '/lol/match/v5/matches/{matchId}' + API_KEY

            x = requests.get(BASE_RIOTAPI_CALL.format(region_v5=region_v5)
              + ACCOUNT_V1_QUERY.format(gamename=gamename, tagline=tagline))

            puuid = x.json()['puuid']
            gamename = x.json()['gameName']
            tagline = x.json()['tagLine']
            y = requests.get(BASE_RIOTAPI_CALL.format(region_v5=region_v5)
              + MATCH_IDS_V5_QUERY.format(puuid=puuid)) # list of 20 match numbers

            # get latest match id by puuid
            latest_match = y.json()[0]
            z = requests.get(BASE_RIOTAPI_CALL.format(region_v5=region_v5)
              + '/' + MATCH_V5_QUERY.format(matchId=latest_match))
                
                # todo iterate through - info[PLAYER_NUMBER].perks[0] (statPerks){"defense", "flex", "offense"}
            # iterate through - metadata.participants[] and save index that matches puuid as PLAYER_NUMBER
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

            # runes_reforged = open(dragontail_filepath
                # + '/dragontail-12.6.1/12.6.1/data/en_US/runesReforged.json')
            # runes_mapping = json.load(runes_reforged)
            runes_reforged_cdn = requests.get('https://ddragon.leagueoflegends.com/cdn/12.6.1/data/en_US/runesReforged.json')
            runes_mapping = runes_reforged_cdn.json()

            ic_pf = "http://ddragon.leagueoflegends.com/cdn/img/"
            file_pf = (dragontail_filepath
            + '/dragontail-12.6.1/img/')

            RUNE_TREES = []
            primarystyle_runes_fileList = []
            substyle_runes_fileList = []
            primary_perk_ddragon_img_urls = []
            substyle_perk_ddragon_img_urls = []
            include_images_by_local_filepath = False

            if (include_images_by_local_filepath):
                # for each Style
                for i in runes_mapping:
                    # if Style is listed as first as primary style in json
                    if i['id'] == style_ids[0]:
                        RUNE_TREES.append(i['key'])
                        primarystyle_runes_fileList.append(discord.File(file_pf + i['icon']))
                        # for each list of runes per Style
                        for j in i['slots']:
                            # for each rune in the list of runes
                            for k in j['runes']:
                                # if the rune shows in the primary perks
                                if k['id'] in perk_ids[0]:
                                    RUNE_TREES.append(k['key'])
                                    primarystyle_runes_fileList.append(discord.File(file_pf + k['icon']))
                                elif k['id'] in perk_ids[1]:
                                    RUNE_TREES.append(k['key'])
                                    substyle_runes_fileList.append(discord.File(file_pf + k['icon']))
                    # if Style is listed as second as sub style in json
                    if i['id'] == style_ids[1]:
                        RUNE_TREES.append(i['key'])
                        substyle_runes_fileList.append(discord.File(file_pf + i['icon']))
                        # for each list of runes per Style
                        for j in i['slots']:
                            # for each rune in the list of runes
                            for k in j['runes']:
                                # if the rune shows in the secondary perks
                                if k['id'] in perk_ids[0]:
                                    RUNE_TREES.append(k['key'])
                                    primarystyle_runes_fileList.append(discord.File(file_pf + k['icon']))
                                elif k['id'] in perk_ids[1]:
                                    RUNE_TREES.append(k['key'])
                                    substyle_runes_fileList.append(discord.File(file_pf + k['icon']))

                                for substyle_rune in substyle_runes_fileList:
                                    primarystyle_runes_fileList.append(substyle_rune)

                                await message.channel.send('Runes for **' + gamename + '**\'s latest match: ' + str(RUNE_TREES), files=primarystyle_runes_fileList)

            elif not (include_images_by_local_filepath):
                for i in runes_mapping:
                    # if Style is listed as first as primary style in json
                    if i['id'] == style_ids[0]:
                        primary_perk_ddragon_img_urls.append(markdown_url(i['key'], ic_pf + i['icon'] + ' '))
                        # for each list of runes per Style
                        for j in i['slots']:
                            # for each rune in the list of runes
                            for k in j['runes']:
                                # if the rune shows in the primary perks
                                if k['id'] in perk_ids[0]:
                                    primary_perk_ddragon_img_urls.append(markdown_url(k['key'], ic_pf + k['icon'] + ' '))
                    # if Style is listed as second as sub style in json
                    if i['id'] == style_ids[1]:
                        substyle_perk_ddragon_img_urls.append(markdown_url(i['key'], ic_pf + i['icon'] + ' '))
                        # for each list of runes per Style
                        for j in i['slots']:
                            # for each rune in the list of runes
                            for k in j['runes']:
                                # if the rune shows in the secondary perks
                                if k['id'] in perk_ids[1]:
                                    substyle_perk_ddragon_img_urls.append(markdown_url(k['key'], ic_pf + k['icon'] + ' '))
                
                for secondary_rune in substyle_perk_ddragon_img_urls:
                    primary_perk_ddragon_img_urls.append(secondary_rune)

                await message.channel.send('Runes for **' + gamename + '**\'s latest match: ')
                for rune in primary_perk_ddragon_img_urls:
                    await message.channel.send(rune)

        if message.content == 'ping':
            await message.channel.send('pong')

def markdown_url(description, url):
    description = '[' + description + ']'
    hyperlink = '(' + url + ')'
    return description + hyperlink

bot.run(discord_bot_token_id) # discord bot token id

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(discord_bot_token_id)