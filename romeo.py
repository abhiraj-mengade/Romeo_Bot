import os
import discord
from dotenv import load_dotenv
import json
import requests
import random
from keep_alive import keep_alive

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
  if(type(json_data)==dict):
      return "**Wrong Word da!**"
  pos = json_data[0]["meanings"][0]["partOfSpeech"]
  defn = json_data[0]["meanings"][0]["definitions"][0]["definition"]
  phonetic = json_data[0]["phonetic"]
  example = json_data[0]["meanings"][0]["definitions"][0]["example"]
  s = "**"+s.upper()+"**\n\n"+"**Part Of Speech:**"+" *"+pos+"*\n"+"**Defn:**"+" *"+defn+"*\n"+"**Phonetic:**"+" *"+phonetic+"*\n"+"**Example:**"+" *"+example+"*\n"

  return(s)

def get_syn(s):
  response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+s)
  json_data = json.loads(response.text)
  if(type(json_data)==dict):
      return "**Wrong Word da!**"
  syn = json_data[0]["meanings"][0]["definitions"][0]["synonyms"]
  s = "**"+s.upper()+"**\n\n"
  for i in range(len(syn)//2):
      s += "***"+syn[i]+"***\n"
  return s

def get_anty(s):
  response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+s)
  json_data = json.loads(response.text)
  if(type(json_data)==dict):
      return "**Wrong Word da!**"
  anty = json_data[0]["meanings"][0]["definitions"][0]["antonyms"]
  s = "**"+s.upper()+"**\n\n"
  for i in range(len(anty)):
      s += "***"+anty[i]+"***\n"
  return s

def get_org(s):
  response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+s)
  json_data = json.loads(response.text)
  if(type(json_data)==dict):
      return "**Wrong Word da!**"
  org="**No Origin!**"
  if("origin" in json_data[0]):
      org = json_data[0]["origin"]
  return org

def get_ana(s):
  if(len(s))>9:
       return "**Enter a word which has less than 10 characters!**"
  response = requests.get("http://www.anagramica.com/best/:"+s)
  json_data = json.loads(response.text)
  ana = json_data["best"]
  s = "**"+s.upper()+"**\n\n"
  for i in range(len(ana)):
      s += "***"+ana[i]+"***\n"
  return s


help = """
***🤖 ROMEO's HELP MENU 🤖 *** 

**r.help - You know what this does!**

**r.dict <word> - Displays definition, phonetic and Type of the word**

**r.syn <word> - Displays synonyms of the word**

**r.anty <word> - Displays antonyms of the word**

**r.org <word> - Displays Origin of the word**

**r.ana <word> - Displays a list of Anagrams of the word**

**r.quote - Displays a curious random quote & an image!**
"""

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  if msg.startswith("r.help"):
      embedVar = discord.Embed(title="Romeo 👑", description=help, color=0x00ff00)
      await message.channel.send(embed=embedVar)

  if msg.startswith("r.hello"):
    embedVar = discord.Embed(title="Romeo 👑", description="*Ahoy! Nice to see ya mate* :)", color=0x00ff00)
    await message.channel.send(embed=embedVar)

  if msg.startswith("r.quote"):
    quote = "***"+get_quote()+"***"
    embedVar = discord.Embed(title="Quote ✒️", description=quote +"\n\n"+ "https://picsum.photos/500", color=0x00ff00)
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

      embedVar = discord.Embed(title="Antonyms 🛠", description=file, color=0x00ff00)
      await message.channel.send(embed=embedVar)

  if msg.startswith("r.org"):
      l = msg.split()
      if(len(l)==1):
          file="**Enter the word da!**"
      else:
          file = get_org(l[1])

      embedVar = discord.Embed(title="Origin 🌾", description=file, color=0x00ff00)
      await message.channel.send(embed=embedVar)

  if msg.startswith("r.ana"):
      l = msg.split()
      file = get_ana(l[1])
      embedVar = discord.Embed(title="Anagram 🧣", description=file, color=0x00ff00)
      await message.channel.send(embed=embedVar)

keep_alive()
client.run(TOKEN)