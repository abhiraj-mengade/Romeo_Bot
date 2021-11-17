#imports
import os
import discord
from dotenv import load_dotenv
import json
import requests
import random
from keep_alive import keep_alive

#Setting the Client & Loading the TOKEN
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

"""
get_quote():
Gets a random quote from the zenquotes api and returns back a string.
"""
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  return(quote)

"""
get_dict(s):
Takes input of a string and request data from the dictionary api.
Returns a string including, Part of Speech, Definition, Phonetic, origin and Example of the word.
"""
def get_dict(s):
  response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+s)
  json_data = json.loads(response.text)
  if(type(json_data)==dict):
      return "**Wrong Word da!**"
  pos = json_data[0]["meanings"][0]["partOfSpeech"]
  defn = json_data[0]["meanings"][0]["definitions"][0]["definition"]
  phonetic = json_data[0]["phonetic"]
  example = json_data[0]["meanings"][0]["definitions"][0]["example"]
  org="**No Origin!**"
  if("origin" in json_data[0]):
      org = json_data[0]["origin"]
  s = "**"+s.upper()+"**\n\n"+"**Part Of Speech:**"+" *"+pos+"*\n"+"**Defn:**"+" *"+defn+"*\n"+"**Phonetic:**"+" *"+phonetic+"*\n"+"**Example:**"+" *"+example+"*\n""**Origin:**"+" *"+org+"*\n"
  syn = json_data[0]["meanings"][0]["definitions"][0]["synonyms"]
  anty = json_data[0]["meanings"][0]["definitions"][0]["antonyms"]
  s+="**Synonyms:**\n"
  for i in range(min(len(syn),3)):
      s += "*"+syn[i]+"*\n"
  s+="**Antonyms:**\n"
  for i in range(min(len(anty),3)):
      s += "*"+anty[i]+"*\n"
  return(s)


"""
get_defn(s):
Takes input of a string and request data from the dictionary api.
Returns a string with definition and phonetic of the word.
"""
def get_defn(s):
  response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+s)
  json_data = json.loads(response.text)
  if(type(json_data)==dict):
      return "**Wrong Word da!**"
  pos = json_data[0]["meanings"][0]["partOfSpeech"]
  phonetic = json_data[0]["phonetic"]
  defn = json_data[0]["meanings"][0]["definitions"][0]["definition"]
  s = "**"+s.upper()+"**\n\n"+"**Part Of Speech:**"+" *"+pos+"*\n"+"**Defn:**"+" *"+defn+"*\n"+"**Phonetic:**"+" *"+phonetic+"*\n"
  return s

"""
get_syn(s):
Takes input of a string and request data from the dictionary api.
Returns a string with synonyms of the word.
"""
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

"""
get_anty(s):
Takes input of a string and request data from the dictionary api.
Returns a string with antonyms of the word.
"""
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


"""
get_origin(s):
Takes input of a string and request data from the dictionary api.
Returns a string with the origin of the word.
"""
def get_org(s):
  response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+s)
  json_data = json.loads(response.text)
  if(type(json_data)==dict):
      return "**Wrong Word da!**"
  org="**No Origin!**"
  if("origin" in json_data[0]):
      org = json_data[0]["origin"]
  return org

"""
get_ana(s):
Takes input of a string and request data from the dictionary api.
Returns a string with anagrams of the word.
"""
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

#message displayed by help text
help = """
***🤖 ROMEO's HELP MENU 🤖 *** 

**r.help - You know what this does!**

**r.dict <word> - Displays definition, phonetic, Type, origin, synonyms & antonyms of the word**

**r.defn <word> - Displays definition, phonetic and Type of the word**

**r.syn <word> - Displays synonyms of the word**

**r.anty <word> - Displays antonyms of the word**

**r.org <word> - Displays Origin of the word**

**r.ana <word> - Displays a list of Anagrams of the word**

**r.quote - Displays a curious random quote & an image!**

**Made by - Abhiraj Mengade :)**
"""

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  #storing the user message
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


  
  if msg.startswith("r.defn"):
      l = msg.split()
      if(len(l)==1):
          file="**Enter the word da!**"
      else:
          file = get_defn(l[1])
      embedVar = discord.Embed(title="Definition 🖊", description=file, color=0x00ff00)
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


#flask server function
keep_alive()
#client run function
client.run(TOKEN)