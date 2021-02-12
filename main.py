import discord
import data
import nest_asyncio
import sys

nest_asyncio.apply()

TOKEN = 'ODA5NDg4OTMyODMxNzU2MzEw.YCV1UQ.S15uTMohLBkvn8r4NrUeGUCBO54'

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!binflip'):
    	try:
    		args = message.content.split(" ")
    		await message.channel.send("Please wait a few minutes...")
    		binList = data.dataMain(int(args[1]), int(args[2]))
    		totalItems = int(args[1])
    		currentItemsInMsg = 0
    		for i in range(0, totalItems):
    			if (currentItemsInMsg == 0):
    				embedVar = discord.Embed(title="Biggest BIN Differences", color=0x4CFCFF)
    			if (currentItemsInMsg < 12):
    				nameData = str(i + 1) + ". " + binList[i][0]
    				valueData = "```Rarity: " + binList[i][1] + "\nCategory: " + binList[i][2] + "\nLowest Price: " + binList[i][3] + "\n2nd Lowest Price: " + binList[i][4] + "\nDifference: " + binList[i][5] + "```"
    				embedVar.add_field(name = nameData, value = valueData, inline= True)
    				currentItemsInMsg += 1
    			if (currentItemsInMsg == 12 or (i == totalItems - 1)):
    				await message.author.send(embed=embedVar)
    				currentItemsInMsg = 0
    		await message.channel.send("Check your DMs {}!".format(message.author.name))
    	except: 
    		await message.channel.send("Bot crashed! Bad arguments?")


    if message.content.startswith('!die'):
    	await client.logout()

client.run(TOKEN)