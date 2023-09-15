import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="$", intents = intents)
msg = None
m = None


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return
#
#    if message.content == 'ip' or message.content == 'Ip' or message.content == 'IP' or message.content == 'iP'\
#        or message.content == ' ip' or message.content == 'ip ':
#        ip = str(fetchip() + ':25565')
#        user = await client.fetch_user(message.author.id)
#        await user.send(ip)
#        await message.delete()

@client.event
async def on_message(message):
    global msg, running
    if message.author != client.user:
        temp = True
        channel = message.channel
        if message.content == '!startIPbot':
            running = True
            async for b in channel.history(limit=100):
                if b.author == client.user:  # client.user or bot.user according to what you have named it
                    await b.delete()

            #msg = await channel.send('Send me that ✅ reaction, to get the Minecraft ip')
            #await msg.add_reaction('✅')
            await message.delete()

        elif message.content == '!start':
            running = True
            #msg = await channel.send('Send me that ✅ reaction, to get the Minecraft ip')
            await message.delete()
            #await msg.add_reaction('✅')


        elif message.content == '!stop':
            running = False
            if msg is not None:
                await message.delete()
                await msg.delete()
                return
                #quit(0)

        else:
            if msg is not None:
                temp = False
                omsg = msg
                # await msg.delete()
        if running:

            msg = await channel.send('Send me that ✅ reaction, to get the Minecraft ip')
            await msg.add_reaction('▫️')
            await msg.add_reaction('✅')

            if not temp:
                await omsg.delete()



@client.event
async def on_reaction_add(reaction, user):

    global msg, m
    if msg is not None and user != client.user and reaction.emoji == "✅":

        ip = str(fetchip() + ':25565')

        #user = await client.fetch_user(reaction.author.id)
        m = await user.send("...")
        dmchannel =  m.channel # dm channel you want to clear
        async for message in dmchannel.history(limit=100):
            if message.author == client.user:  # client.user or bot.user according to what you have named it
                await message.delete()

        m = await user.send(ip)

        await msg.clear_reaction('✅')
        await msg.add_reaction('✅')



def fetchip():
    r = requests.get( 'https://ipinfo.io/ip', auth=('user', 'pass'))
    return r.text

client.run('HERE YOUR DISCORD TOKEN')
