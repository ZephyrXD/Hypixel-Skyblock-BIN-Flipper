import asyncio
import aiohttp
import time
import requests
import nbt
import io
import base64

def getUrls():
	firstUrl = ["https://api.hypixel.net/skyblock/auctions?page=0"]
	firstPage = asyncio.run(getData(firstUrl))
	firstPage = firstPage[0]
	totalPage = firstPage["totalPages"]
	urls = []
	currentPage = 0
	while currentPage <= totalPage:
		urls.append("https://api.hypixel.net/skyblock/auctions?page=" + str(currentPage))
		currentPage += 1
	return urls

async def get(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                resp = await response.json()
                return resp
                print("Successfully got url {}.".format(url))
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))


async def getData(urls):
    ret = await asyncio.gather(*[get(url) for url in urls])
    return ret

def binFlip(allAuctions, budget):

	items = {} # {RawName: [currentName, rarity, category, firstPrice, secondPrice, coinDifference}
	for page in allAuctions:
		auctions = page["auctions"]
		for x in auctions:
			try:
				if x["bin"]:
					itemName = getRawName(x["item_bytes"])
					if (x["item_name"] != "null" and x["category"] != "misc" and x["category"] != "blocks" and x["starting_bid"] < budget):
						if itemName in items:
							itemData = items[itemName]
							if itemData[4] == " ":
								if x["starting_bid"] <= int(itemData[3]):
									itemData[0] = x["item_name"]
									itemData[1] = x["tier"]
									itemData[4] = itemData[3]
									itemData[3] = str(x["starting_bid"])
									items[itemName] = itemData
								else: 
									itemData[4] = str(x["starting_bid"])
									items[itemName] = itemData
							else:
								if (x["starting_bid"] <= int(itemData[3])):
									itemData[4] = itemData[3]
									itemData[3] = str(x["starting_bid"])
									itemData[0] = x["item_name"]
									itemData[1] = x["tier"]
									items[itemName] = itemData
								else: 
									if (x["starting_bid"] > int(itemData[3]) and x["starting_bid"] < int(itemData[4])):
										itemData[4] = x["starting_bid"]
										items[itemName] = itemData
						else:
							items[itemName] = [x["item_name"], x["tier"], x["category"], str(x["starting_bid"]), " "," "]
			except KeyError:
				pass
	#Calculations and remove not wanted stuffs
	finalItems = {}
	for key in items.keys():
		try:
			dataList = items[key]
			dataList[5] = str(int(dataList[4]) - int(dataList[3]))
			finalItems[key] = dataList
		except:
			pass
	for key, value in sorted(finalItems.items(), key=lambda e: int(e[1][5]), reverse = True):
		print (key, value)
						
##### NBT Data #####
def getRawName(raw):
   data = nbt.nbt.NBTFile(fileobj = io.BytesIO(base64.b64decode(raw)))
   return str(data['i'].tags[0]['tag']['ExtraAttributes']['id'])
##### NBT Data #####

def main():
	print("Downloading data...", end = '')
	urls = getUrls()
	start = time.time()
	data = asyncio.run(getData(urls))
	print("Done!\nParsing data...", end = '')
	#Testing
	binFlip(data, 3000000)
	print("Done!")
	#Testing End
	end = time.time()

main()
