import discord
import os
from discord.colour import Color
from discord.ext import commands
import price_util as pu
import util
from sigfig import round

client = discord.Client()
bot = commands.Bot(command_prefix='-doge')
firstEmbed = None
thirdEmbed = None
secondEmbed = None
tmpMsg = None


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(msg):

    if msg.author == client.user:
        return

    msgContent = msg.content
    msgArr = msgContent.split()
    channel = msg.channel

    if msgContent.startswith('-doge'):
        if len(msgArr) == 2:
            chanMsg = await channel.send(embed=discord.Embed(title="Loading..."))
            displayLeftArrow = False
            [name, rank, price, timestamp, price_change_pct,
                price_change, high, logo_url] = pu.getBasic(msgArr[1])
            [desp, coinUrl] = pu.getUrl(msgArr[1])
            if len(desp) > 2048:
                desp = desp[:2047]

            if len(desp) >= 400:
                showDesp = desp[:400] + \
                    "......(for more information, react with \U00002B05 in bottom)"
                displayLeftArrow = True
            else:
                showDesp = desp

            embed = discord.Embed(title=msgArr[1]+" ("+name+")", url=coinUrl,
                                  description=showDesp, color=discord.Color.blue())
            embed.add_field(name="Current Price",
                            value=str(round(float(price), sigfigs=7))+" USD", inline=True)
            newTimestamp = util.convertTimestamp(timestamp)
            embed.add_field(name="Timestamp", value=newTimestamp, inline=True)
            embed.add_field(name="Price Change in 1 Day", value=str(
                round(float(price_change), sigfigs=7)), inline=False)
            embed.add_field(name=f"Price Change % in 1 Day", value=str(
                round(float(price_change_pct), sigfigs=5))+"%", inline=False)
            embed.add_field(name="Rank by Market Cap", value=rank, inline=True)
            embed.add_field(name="All Time High Price", value=str(
                round(float(high), sigfigs=7))+" USD", inline=True)
            embed.set_thumbnail(
                url=logo_url)
            leftString = ""
            if displayLeftArrow:
                leftString = "\U00002B05Go Left for Description    "

            embed.set_footer(
                text=leftString+"Go Right for Sparkline\U000027A1")

            await msg.add_reaction('\U0001F4B0')
            await chanMsg.edit(embed=embed)
            await chanMsg.add_reaction('\U00002B05')
            await chanMsg.add_reaction('\U000027A1')

            # set embeds
            global secondEmbed
            secondEmbed = embed
            global firstEmbed
            firstEmbed = discord.Embed(title=msgArr[1]+" ("+name+")", url=coinUrl,
                                       description=desp, color=discord.Color.gold())
            global thirdEmbed
            [today, oldday] = util.thirtyDayInterval(timestamp)
            # print([today, oldday])
            pu.visualize(pu.getSparkline(msgArr[1], oldday, today))
            thirdEmbed = discord.Embed(
                title="Visual Representation", description="Market Price for Past 30 Days", color=discord.Color.purple())

        else:
            await channel.send('Please at least enter one crypto currency')
    await bot.process_commands(msg)


@client.event
async def on_reaction_add(reaction, user):
    global tmpMsg
    if user == client.user:
        return
    if reaction.emoji == '\U00002B05':
        # from second to first
        if reaction.message.embeds[0].colour == discord.Color.blue():
            await reaction.message.edit(embed=firstEmbed)
            await reaction.remove(user)
            return
        # from third to second
        if reaction.message.embeds[0].colour == discord.Color.purple():
            await reaction.message.edit(embed=secondEmbed)
            await tmpMsg.delete()
            await reaction.remove(user)
            return
        await reaction.remove(user)

    elif reaction.emoji == '\U000027A1':
        # from second to third
        if reaction.message.embeds[0].colour == discord.Color.blue():
            await reaction.message.edit(embed=thirdEmbed)
            tmpMsg = await reaction.message.channel.send(file=discord.File('sparkline.png'))
            await reaction.remove(user)
            return

        # from first to second
        if reaction.message.embeds[0].colour == discord.Color.gold():
            await reaction.message.edit(embed=secondEmbed)
            await reaction.remove(user)
            return
        await reaction.remove(user)


client.run(os.getenv('DISCORD_TOKEN'))
