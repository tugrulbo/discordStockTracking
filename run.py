from email import message
import glob
import json
from pydoc import cli
import discord
from discord.ext import commands
from discord.ext import tasks
from numpy import double
from config import token
from hepsiburada import Hepsiburada
import asyncio

from trendyol import Trendyol

prefix = "."

bot = commands.Bot(command_prefix=prefix)

client = discord.Client()


@bot.event
async def on_ready():
    print("--------------Bot Hazır---------------")
    await client.loop.create_task(checkProducts())


async def checkProducts():
    global trackerList
    trackerList = []
    print("checkProduct")
    # trackerList altındaki bütün dosyalar okunacak
    # ardından teker teker dosyalar okunacak
    # her dosya okunduktan sonra trackerList içine aktarılacak buradan bütün url adresleri kontrol edilecek
    # trackerList içinden url adresi alınarak üründen gerekli olan kısımların tamamı okunacak
    # seçilen fiyat karışılaştırması yapılacak eğer indirim oranı belirtilen ürün altında ise discord a mesaj gönderilecek
    # şuanda ürün bulma sistemi id üzerinden ve isim üzerinden çalışıyor.
    # ürün sistemine url ile tarama yapılması kısmının eklenmesi lazım

    files = glob.glob("trackerList/*.json")
    fileSize = len(files)
    while(fileSize > 0):
        print("File size: {}".format(fileSize))
        for i in range(fileSize):
            with open(files[i], "r", encoding="utf-8") as f:
                trackerList = json.loads(f.read())

            print("TrackerList: {}".format(len(trackerList)))
            # url parçalanıp oradan hangi tür olduğu anlaşılacak.
            for product in trackerList:
                urlType = product["url_type"]
                if(urlType.lower() == "hepsiburada"):
                    product_id = product["url"]
                    productModel = Hepsiburada.findProduct(product_id)

                    if "," in productModel.price:
                        productPriceArray = productModel.price.split(",")

                        productPrice = productPriceArray[0].replace(".", "")
                    else:
                        productPriceArray = productModel.price.replace(".", "")

                    if(float(productPrice) < float(product["defaultPrice"])):

                        msg = "Ürün Fiyati Düştü {} -> {}".format(
                            productModel.price, product["defaultPrice"])
                        channel = await bot.fetch_channel(962153155179737129)
                        embedVar = discord.Embed(
                            title="ÜRÜN FİYATI DÜŞTÜ", description="", color=0x00ff00)
                        embedVar.add_field(name="Ürün Adı", value="{}".format(
                            productModel.title), inline=False)
                        embedVar.add_field(
                            name="Ürün Fiyatı", value=msg, inline=False)
                        embedVar.add_field(name="Link", value="{}".format(
                            productModel.url), inline=False)
                        await channel.send(embed=embedVar)

                elif(urlType.lower() == "trendyol"):
                    product_id = product["url"]
                    productModel = Trendyol.findProduct(product_id)

                    if "," in productModel.price:
                        productPriceArray = productModel.price.split(",")

                        productPrice = productPriceArray[0].replace(".", "")
                    else:
                        productPriceArray = productModel.price.replace(".", "")

                    if(float(productPrice) < float(product["defaultPrice"])):

                        msg = "Ürün Fiyati Düştü {} -> {}".format(
                            productModel.price, product["defaultPrice"])
                        channel = await bot.fetch_channel(962153155179737129)
                        embedVar = discord.Embed(
                            title="ÜRÜN FİYATI DÜŞTÜ", description="", color=0x00ff00)
                        embedVar.add_field(name="Ürün Adı", value="{}".format(
                            productModel.title), inline=False)
                        embedVar.add_field(
                            name="Ürün Fiyatı", value=msg, inline=False)
                        embedVar.add_field(name="Link", value="{}".format(
                            productModel.url), inline=False)
                        await channel.send(embed=embedVar)


bot.load_extension('cogs.CommandsEvents')
bot.run(token)
