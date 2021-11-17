import os
import discord
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("/hello"):
    await message.channel.send("Hello! I am Romeo :)")
    await message.channel.send('https://picsum.photos/'+ str(random.randint(500,1000)))

client.run(TOKEN)