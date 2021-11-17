import os
import discord
from dotenv import load_dotenv
import json
import requests
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  return(quote)


def get_dict(s):
  response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+s)
  json_data = json.loads(response.text)
  pos = json_data[0]["meanings"][0]["partOfSpeech"]
  defn = json_data[0]["meanings"][0]["definitions"][0]["definition"]
  phonetic = json_data[0]["phonetic"]
  example = json_data[0]["meanings"][0]["definitions"][0]["example"]
  s = "**"+s.upper()+"**\n\n"+"**Part Of Speech:**"+" *"+pos+"*\n"+"**Defn:**"+" *"+defn+"*\n"+"**Phonetic:**"+" *"+phonetic+"*\n"+"**Example:**"+" *"+example+"*\n"

  return(s)

def get_syn(s):
  response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+s)
  json_data = json.loads(response.text)
  syn = json_data[0]["meanings"][0]["definitions"][0]["synonyms"]
  s = "**"+s.upper()+"**\n\n"
  for i in range(len(syn)//2):
      s += "***"+syn[i]+"***\n"
  return s

def get_anty(s):
  response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+s)
  json_data = json.loads(response.text)
  anty = json_data[0]["meanings"][0]["definitions"][0]["antonyms"]
  s = "**"+s.upper()+"**\n\n"
  for i in range(len(anty)):
      s += "***"+anty[i]+"***\n"
  return s

def get_org(s):
  response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+s)
  json_data = json.loads(response.text)
  org = json_data[0]["origin"]
  return org


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  if msg.startswith("r.help"):
      embedVar = discord.Embed(title="Romeo 👑", description="*I gotchya back bro* :)", color=0x00ff00)
      await message.channel.send(embed=embedVar)

  if msg.startswith("r.hello"):
    embedVar = discord.Embed(title="Romeo 👑", description="*Ahoy! Nice to see ya mate* :)", color=0x00ff00)
    await message.channel.send(embed=embedVar)

  if msg.startswith("r.quote"):
    quote = "***"+get_quote()+"***"
    embedVar = discord.Embed(title="Quote ✒️", description=quote, color=0x00ff00)
    await message.channel.send(embed=embedVar)
    await message.channel.send('https://picsum.photos/'+ str(random.randint(500,1000)))

  if msg.startswith("r.dict"):
      l = msg.split()
      if(len(l)==1):
          file="**Enter the word da!**"
      else:
          file = get_dict(l[1])

      embedVar = discord.Embed(title="Dictionary 📘", description=file, color=0x00ff00)
      await message.channel.send(embed=embedVar)

  if msg.startswith("r.syn"):
      l = msg.split()
      if(len(l)==1):
          file="**Enter the word da!**"
      else:
          file = get_syn(l[1])

      embedVar = discord.Embed(title="Synonym 🖇", description=file, color=0x00ff00)
      await message.channel.send(embed=embedVar)

  if msg.startswith("r.anty"):
      l = msg.split()
      if(len(l)==1):
          file="**Enter the word da!**"
      else:
          file = get_anty(l[1])

      embedVar = discord.Embed(title="Antonyms 🛠 ", description=file, color=0x00ff00)
      await message.channel.send(embed=embedVar)

  if msg.startswith("r.org"):
      l = msg.split()
      if(len(l)==1):
          file="**Enter the word da!**"
      else:
          file = get_org(l[1])

      embedVar = discord.Embed(title="Origin 🛠 ", description=file, color=0x00ff00)
      await message.channel.send(embed=embedVar)


client.run(TOKEN)