Practice using python to create a simple Discord bot

This bot will respond to the following commands:
\_runes "*gamename*#*tagline*" (region) | ex: `_runes "Lee Sin#NA1" americas`
 * shows the runes used from a summoner's latest match

Setup:
You will need to create a discord app in https://discord.com/developers/applications and assign a bot to the app
Record the **bot's token-id** on app creation as it may not be accessible later for security reasons used in `token_file.py` to wake up the bot
Use the invite link to invite the bot to a server
For python language Discord bot documentation:
 - https://discordpy.readthedocs.io/en/latest/api.html
For Discord language agnostic bot documentation:
 - https://discord.com/developers/docs/quick-start/getting-started
For **Riot API api_key** and testing:
 - https://developer.riotgames.com/ for api_key
 - https://developer.riotgames.com/apis for testing
For runes images: Download ddragon and set the ddragon filepath in index.py or reference online content delivery network's (CDN) latest version:
 - https://riot-api-libraries.readthedocs.io/en/latest/ddragon.html

1. install python
 - https://www.python.org/downloads/
2. install requests and discord.py for python
 * python commands for windows:
  - `py -3 -m pip install requests`
  - `py -3 -m pip install discord.py`
3. Insert discord and riot secrets into **token_file.py** in the same folder as **index.py**
``` python
api_key = 'RGAPI-00xx0000-0000-0000-x0x0-00000000x0xx'
discord_bot_token_id = 'XXXxXxX0XxX0XXXxXXx0XxXx.XxXx0x.xxX0xxXXxXxxXx0x00XXxXxxxXxXXxXXxx0xXX'
```
4. Run **index.py** to wake the bot on the server
 - `py index.py`