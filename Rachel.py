import discord
import asyncio
import datetime
import os
import re
import urllib
import sys, traceback
import requests, time
from discord.utils import get
client = discord.Client()
url=''
botOwner = "266640111897149440"

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="!help", type=1))
    client.loop.create_task(check_new_animes())
    Channel = client.get_channel('503638566405013505')
    Text= "Welcome to **Otaku World** Discord server! <:Hehe:503632223895945227>\nIf you watch **anime** react with <:TohruPoint:503633376524107776> to join **anime** group.\nIf you read **manga** react with <:NekoChen:503633274594394123> to join **manga** group."
    Moji = await client.send_message(Channel, Text)
    emoji1 = get(client.get_all_emojis(), name='TohruPoint')
    emoji2 = get(client.get_all_emojis(), name='NekoChen')
    await client.add_reaction(Moji, emoji=emoji1)
    await client.add_reaction(Moji, emoji=emoji2)

async def check_new_animes():
    lastAnime = eval(requests.get("http://animeslayer.com/Data/newSystem/NewGet.php?fu=1").content)[0]
    while(True):
        newAnime = eval(requests.get("http://animeslayer.com/Data/newSystem/NewGet.php?fu=1").content)[0]
        if newAnime == lastAnime:
            print("No new episode")
        else:
            print("New episode")
            lastAnime = eval(requests.get("http://animeslayer.com/Data/newSystem/NewGet.php?fu=1").content)[0]
            AnimeLogChannel = discord.Object(id=504382218961944607)
            embed=discord.Embed(color=0xffa500)
            embed.add_field(name="Title: " , value=str(lastAnime["Title"]), inline=True)
            embed.add_field(name="State: " , value=str(lastAnime["State"]), inline=True)
            embed.add_field(name="Year: " , value=str(lastAnime["Year"]), inline=True)
            embed.add_field(name="Rate: " , value=str(lastAnime["Rate"]), inline=True)
            embed.add_field(name="Gen: " , value=str(lastAnime["Gen"].replace("[","").replace('"',"").replace("]","").replace(",",", ")), inline=True)
            embed.add_field(name="Time: " , value=str(lastAnime["time"].replace(",- ", "")), inline=True)
            if lastAnime["Rating"] == "":
                embed.add_field(name="Rating: " , value="-", inline=True)
            else:
                embed.add_field(name="Rating: " , value=str(lastAnime["Rating"]), inline=True)
            embed.set_image(url=(str(lastAnime["img"])).replace("\\",""))
            try:
                await client.send_message(AnimeLogChannel, embed=embed)
            except discord.HTTPException:
                print(embed.to_dict())
                raise
        lastAnime = newAnime
        await asyncio.sleep(1)

@client.event
async def on_message(message):
    now = datetime.datetime.now()
    if message.channel.id == "504690754669510667":
        if message.content.startswith("!invite"):
            await client.send_message(message.channel, "Invite link: https://discord.gg/xDWGavx")
    if message.author.id == botOwner:
        if message.content.startswith("!clear"):
            mm=message.content.split('!clear ')[1]
            nn=0
            async for m in client.logs_from(message.channel, limit=int(mm)):
                await client.delete_message(m)
                nn+=1
            embed=discord.Embed(title="<a:cleaning:521720398740717569> The chat is clean:", description=str(nn)+" messages deleted.", color=0xffa500)
            embed.set_footer(text=now.strftime("%Y/%m/%d %H:%M:%S"))
            n = await client.send_message(message.channel, embed=embed)
            await asyncio.sleep(2)
            await client.delete_message(n)
        if message.content.startswith("!refresh"):
            await client.delete_message(message)
            await client.logout()
            os.system("python Rachel.py")
            exit()
        if message.content.startswith("!lastAnime"):
            lastAnime = eval(requests.get("http://animeslayer.com/Data/newSystem/NewGet.php?fu=1").content)[0]
            AnimeLogChannel = discord.Object(id=504382218961944607)
            embed=discord.Embed(color=0xffa500)
            embed.add_field(name="Title: " , value=str(lastAnime["Title"]), inline=True)
            embed.add_field(name="State: " , value=str(lastAnime["State"]), inline=True)
            embed.add_field(name="Year: " , value=str(lastAnime["Year"]), inline=True)
            embed.add_field(name="Rate: " , value=str(lastAnime["Rate"]), inline=True)
            embed.add_field(name="Gen: " , value=str(lastAnime["Gen"].replace("[","").replace('"',"").replace("]","").replace(",",", ")), inline=True)
            embed.add_field(name="Time: " , value=str(lastAnime["time"].replace(",- ", "")), inline=True)
            if lastAnime["Rating"] == "":
                embed.add_field(name="Rating: " , value="-", inline=True)
            else:
                embed.add_field(name="Rating: " , value=str(lastAnime["Rating"]), inline=True)
            embed.set_image(url=(str(lastAnime["img"])).replace("\\",""))
            try:
                await client.send_message(AnimeLogChannel, embed=embed)
            except discord.HTTPException:
                print(embed.to_dict())
                raise
        if message.content.startswith("AQ!character"):
            await client.delete_message(message)
    if message.author.id == "464004630632988672":
        if message.content.startswith("🎉 "):
            await client.pin_message(message)

@client.event
async def on_member_join(member):
    Role = discord.utils.get(member.server.roles, name="Otaku")
    await client.add_roles(member, Role)
    JoiningLogChannel = discord.Object(id=510846615880335361)
    embed=discord.Embed(description=str(member.mention)+" joined.", color=0xffa500)
    await client.send_message(JoiningLogChannel, embed=embed)

@client.event
async def on_member_remove(member):
    JoiningLogChannel = discord.Object(id=510846615880335361)
    embed=discord.Embed(description=str(member.mention)+" left.", color=0xffa500)
    await client.send_message(JoiningLogChannel, embed=embed)

@client.event
async def on_reaction_add(reaction, user):
    roleChannelId = '503638566405013505'
    if reaction.message.channel.id != roleChannelId:
        return
    if user != client.user:
        if str(reaction.emoji) == "<:TohruPoint:503633376524107776>":
            Role = discord.utils.get(user.server.roles, name="Anime")
            await client.add_roles(user, Role)
        if str(reaction.emoji) == "<:NekoChen:503633274594394123>":
            Role = discord.utils.get(user.server.roles, name="Manga")
            await client.add_roles(user, Role)

@client.event
async def on_reaction_remove(reaction, user):
    roleChannelId = '503638566405013505'
    if reaction.message.channel.id != roleChannelId:
        return
    if user != client.user:
        if str(reaction.emoji) == "<:TohruPoint:503633376524107776>":
            Role = discord.utils.get(user.server.roles, name="Anime")
            await client.remove_roles(user, Role)
        if str(reaction.emoji) == "<:NekoChen:503633274594394123>":
            Role = discord.utils.get(user.server.roles, name="Manga")
            await client.remove_roles(user, Role)


@client.event
async def on_message_delete(message):
    now = datetime.datetime.now()
    if message.author.id != client.user.id:
        channel = discord.Object(id=503636188901539863)
        embed=discord.Embed(color=0xffa500)
        embed.add_field(name="**Message:**" , value=str(message.content), inline=False)
        embed.set_author(name=str(message.author), icon_url=str(message.author.avatar_url))
        embed.set_footer(text="Deleted message in #"+str(message.channel.name)+" at "+now.strftime("%Y/%m/%d %H:%M:%S"))
        await client.send_message(channel, embed=embed)

@client.event
async def on_message_edit(before, after):
    now = datetime.datetime.now()
    if after.author.id != client.user.id:
        channel = discord.Object(id=503636188901539863)
        embed=discord.Embed(color=0xffa500)
        embed.add_field(name="**Before:**" , value=str(before.content), inline=False)
        embed.add_field(name="**After:**" , value=str(after.content), inline=False)
        embed.set_author(name=str(after.author), icon_url=str(after.author.avatar_url))
        embed.set_footer(text="Edited message in #"+str(after.channel.name)+" at "+now.strftime("%Y/%m/%d %H:%M:%S"))
        await client.send_message(channel, embed=embed)

client.run('NTAzNjI2Mzg3MTQwMzc4NjM0.Dq5QDg.SK9utIEQ2EJaMoPvpy9RXvZ6R_k')
