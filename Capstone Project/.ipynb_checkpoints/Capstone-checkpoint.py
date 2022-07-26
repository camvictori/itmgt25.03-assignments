from lib2to3.pgen2 import token
import discord
import requests

TOKEN = 'OTk5NjczMzk1MzYyOTMwNzc5.GAdXaA.H9XdEk1EX29Vw0TX2MjNutj7FMsBqKfh0-zWYI'

client = discord.Client()

#commands
from discord.ext import commands

bot = commands.Bot(command_prefix='.')

access_token = ''

@bot.command()
async def login(ctx, username, password):
    # get the access token
    auth_res = requests.post("https://api-ssl.bitly.com/oauth/access_token", auth=(username, password))
    if auth_res.status_code == 200:
        # if response is OK, get the access token
        global access_token
        access_token = auth_res.content.decode()
        await ctx.send(f'Login to Bitly is successful. Your personal access token is {access_token}.')
    else:
        await ctx.send(f'Login to Bitly is unsuccessful. Please recheck your username and password to get your personal access token.')
        exit()

@bot.command()
async def shorten(ctx, url):
    # construct the request headers with authorization
    headers = {"Authorization": f"Bearer {access_token}"}

    # get the group UID associated with our account
    groups_res = requests.get("https://api-ssl.bitly.com/v4/groups", headers=headers)
    if groups_res.status_code == 200:
        # if response is OK, get the GUID
        groups_data = groups_res.json()['groups'][0]
        guid = groups_data['guid']
    else:
        exit()

    # make the POST request to get shortened URL for `url`
    shorten_res = requests.post("https://api-ssl.bitly.com/v4/shorten", json={"group_guid": guid, "long_url": url}, headers=headers)
    if shorten_res.status_code == 200:
        # if response is OK, get the shortened URL
        link = shorten_res.json().get("link")
    else:
        pass

    await ctx.send(f'The shortened link is {link}.')
    link = ''

@bot.command()
async def token(ctx):
    await ctx.send(f'Your personal access token is {access_token}')

@bot.command()
async def features(ctx):
    embed = discord.Embed(title='Slinky Bot Commands',
                            description='The following are the features to start playing with Slinky!',
                            color=0x76b9f0)
    embed.add_field(name='.login',
                    value="This command is used to log in to your bit.ly account before being able to shorten links. \n\nEnter “.login [username] [password] “ and wait for the bot’s response. \n\nIf the login is successful, the bot will indicate your personal access token.",
                    inline=False)
    embed.add_field(name='.shorten',
                    value='This command is used to shorten URLs into a bit.ly link. Make sure that your login is successful before using this command. \n\nEnter “.shorten [URL] “ to shorten your desired link.',
                    inline=False)
    embed.add_field(name='.features',
                    value='Type in this command to know all of Slinky’s commands and features!',
                    inline=False)
    embed.add_field(name='.greeting',
                    value='Greets the user (a.k.a YOU!)',
                    inline=False)
    embed.add_field(name='.info ',
                    value='Know more about me and my humans (the authors)!',
                    inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
     await ctx.send('Slinky is your handy-dandy friend ready to shorten your long URLs on the go! If you need any more help, feel free to contact my humans @sparky#5400, @boni#6139, @camvictori#7381!')

@bot.command()
async def greeting(ctx):
    await ctx.send('Hello! Ready to play slinky '+ str(ctx.author) + '?')

bot.run(TOKEN)