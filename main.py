import discord
from discord.ext import commands
import requests
import os
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="$", intents=intents)
msg = None
m = None
running = False
McRunning = False

user_role = 'YOUR USER-ROLE HERE'   # must be in lowercase
channel_name = 'THE DISCORD-CHANNEL NAME HERE'  # must be identical to the discord-channel-name
discord_Token = 'YOUR DISCORD TOKEN HERE'       # just copy it here.

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global msg, running
    if message.author != client.user:
        temp = True
        channel = message.channel

        if channel.name != channel_name:
            return

        # replace "discord-role" with the role you want to start or stop the Bot

        if message.content == '!start' and user_role in [y.name.lower() for y in message.author.roles]:
            running = True
            # msg = await channel.send('Send me that ✅ reaction, to get the Minecraft ip')
            await message.delete()
            # await msg.add_reaction('✅')

        elif message.content == '!stop' and user_role in [y.name.lower() for y in message.author.roles]:
            running = False
            if msg is not None:
                await message.delete()
                await msg.delete()
                return


        if running:
            if msg is not None:
                temp = False
                omsg = msg

            msg = await channel.send('Send me that ✅ reaction, to get the Minecraft ip')
            await msg.add_reaction('▫️')
            await msg.add_reaction('✅')

            if not temp and omsg is not None:
                await omsg.delete()


@client.event
async def on_reaction_add(reaction, user):

    global msg, m

    # TODO: here we might want to check if the user clicking has specific

    if msg is not None and user != client.user and reaction.emoji == "✅":

        ip = str(fetchip() + ':25565')

        # user = await client.fetch_user(reaction.author.id)
        m = await user.send("...")
        dmchannel = m.channel   # dm channel you want to clear
        async for message in dmchannel.history(limit=100):
            if message.author == client.user:  # client.user or bot.user according to what you have named it
                await message.delete()

        m = await user.send(ip)

        await msg.clear_reaction('✅')
        await msg.add_reaction('✅')


def fetchip():
    r = requests.get( 'https://ipinfo.io/ip', auth=('user', 'pass'))
    return r.text


client.run(discord_Token)
