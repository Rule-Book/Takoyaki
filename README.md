Practice using python to create a simple Discord bot

Currently this bot can:
-abba List a randomly selected youtube link from 10 of Abba's popular songs
-abbamember List the four members of Abba in a discord embed
-runes Given a riot developer api key, shows the runes used from a summoner's latest match

Setup:
You will need to create a discord app in https://discord.com/developers/applications and assign a bot to the app
Keep the bot's token-id as it's used in index.py to wake up the bot
Use the invite link to invite the bot to a server
For -runes: Download ddragon and set the ddragon filepath in index.py
edit inputs.txt to include personalized data (remove brackets)

install python
install requests and discord.py for python
python commands for windows:
py -3 -m pip install requests
py -3 -m pip install discord.py

Run index.py to wake the bot on the server