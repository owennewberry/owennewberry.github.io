import discord
import os
import random
from replit import db
import requests
import time

os.system('git config --global credential.helper wincred')

#response = requests.get(your_url)
#remaining_requests = response.headers.get('X-RateLimit-Remaining')

numbers = "0123456789"
leaderboard = []
coinflipActive = False

with open("dostotcoin.txt") as f:
  for line in f:
    key = line.split("-")[0]
    strValue = line.split("-")[1]
    value = 0
    for i in range(len(strValue)):
      if strValue[i] in numbers:
        value = value*10
        value += numbers.index(strValue[i])
    db[key] = value
  f.close()

keys = db.keys()

print(keys)

nfts = []
with open("nft.txt") as f:
  for line in f:
    nfts.append(line.split("-"))
print(nfts)

def updateDatabase():
  dst = open("dostotcoin.txt", "w")
  for key in keys:
    dst.write(key+"-"+str(db[key])+"\n")
  dst.close()

updateDatabase()

def checkBalance(author):
  keys = db.keys()
  if author in keys:
    return
  else:
    db[author] = 100

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  author = str(message.author)
  if message.author != client.user:
    for temp in nfts:
      if message.content.count(temp[0]) > 0 and temp[1] != author:
        await message.delete()
    if message.channel.id == 936277008474845224:
      if message.content.startswith("dst balance"):
        checkBalance(author)
        updateDatabase()
        await message.channel.send("You have "+str(db[author])+" DostotCoin in your wallet.")
      if message.content.startswith("dst give"):
        keys = db.keys()
        value = 0
        for key in keys:
          if message.mentions[0].name+"#"+message.mentions[0].discriminator == key:
            placeholder = 0
            for i in range(len(message.content)):
              if message.content[i] == " ":
                placeholder = i
            for i in range(placeholder,len(message.content)):
              if message.content[i] in numbers:
                value = value*10
                value += numbers.index(message.content[i])
            if value < db[author] or value == db[author]:
              db[author] -= value
              db[key] += value
              updateDatabase()
              await message.channel.send("Transfer complete!")
            else:
              await message.channel.send("Error: insufficient funds!")
      if message.content.startswith("dst leaderboard"):
        place = 1
        mes = ""
        keys = db.keys()
        list = []
        for x in keys:
          list.append(str(x))
        list.remove("mineshaft")
        value = 0
        leaderboard = []
        while len(list) > 0:
          k = ""
          value = -1
          for key in list:
           if db[key] > value:
             k = key
             value = db[key]
          leaderboard.append(str(place)+". "+k+" - "+str(value)+" D$T")
          place += 1
          list.remove(k)
        for placer in leaderboard:
          mes = mes+placer+"\n"
        updateDatabase()
        await message.channel.send(mes)

    if message.channel.id == 936319285616312432:
      if message.content == str(db["mineshaft"]+1):
        db["mineshaft"]+= 1
        db[author]+= 1
        updateDatabase()
      else:
        await message.channel.send("Chain is broken! Last known value is "+str(db["mineshaft"])+"!")

    if message.channel.id == 937565031061676033:
      if message.content.startswith("dst coinflip"):
        bet = 0
        winSide = ""
        invalid = False
        if random.randint(0,1) == 0:
          coinflip = "Heads"
        else: coinflip = "Tails"
        mes = message.content.split()
        userSide = mes[3]
        if userSide.lower() == "h": winSide = "Heads"
        elif userSide.lower() == "t": winSide = "Tails"
        else:
          invalid = True
          await message.channel.send("Error!")
        betStr = mes[2]
        for i in range(len(betStr)):
          if betStr[i] in numbers:
            bet = bet*10
            bet += numbers.index(betStr[i])
          else: await message.channel.send("Error!")
        if bet > db[author]:
          await message.channel.send("Error: insufficient funds!")
        else:
          if winSide == coinflip:
            db[author] += bet
            checkBalance(author)
            updateDatabase()
            await message.channel.send("It was "+coinflip+"! You won "+str(bet)+" D$T!"+"\n"+"You have "+str(db[author])+" DostotCoin in your wallet.")
          elif invalid == True:
            invalid = False
          else:
            db[author] -= bet
            checkBalance(author)
            updateDatabase()
            await message.channel.send("It was "+coinflip+"! You lost "+str(bet)+" D$T!"+"\n"+"You have "+str(db[author])+" DostotCoin in your wallet.")

    if message.channel.id == 937729708991324190:
      messageList = message.content.split()
      print(messageList)
      if messageList[0] == "dst" and messageList[1] == "NFT" and db[author] > 9999:
        nft = messageList[2]
        nftList = open("nft.txt", "a")
        nftList.write(nft+"-"+author+"\n")
        nftList.close()
        db[author] -= 10000
        updateDatabase()
  os.system('git commit -a -m "Describe your commit here"')
  os.system('git push')
  time.sleep(.25)

time.sleep(.25)

client.run(os.environ['TOKEN'])
