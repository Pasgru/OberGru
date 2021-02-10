#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import discord

TOKEN = 'ODA5MDQ0NTI1OTc5Nzk1NTE2.YCPXbg.bsI5xw4xptn1n-GBB5yJFk2D9OI'

client = discord.Client()

server_id = 143706554703675392  # Weinfeinschmecker ID
category_id = 809128207805710397  # Beta ID

global category
random.seed()

allowed_list = [
    "youtube.com/watch",
    "youtu.be",
    "redd.it",
    "imgur.com",
    ".png",
    ".jpg"
]

moderated_channels = [
    547000766779490304,  # schwarzes-brett
    784923413663580160,  # küchenpass
    761591445156659272  # feldstüberl
]

prefix = ["Feld", "Bauern", "Blumen", "Wein", "Bier", "Holz", "Stein", "Schnitzl"]

suffix = ["stüberl", "kammerl", "hütte", "wiesn", "keller", "saal", "loch", "kabinett"]


@client.event
async def on_ready():
    global category
    print(f'{client.user} has connected to Discord!')
    guild = next(g for g in client.guilds if g.id == server_id)
    category = next(c for c in guild.categories if c.id == category_id)

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='over the inn'))


@client.event
async def on_message(message):
    for channel in moderated_channels:
        if message.channel.id == channel:
            for link in allowed_list:
                if link in message.content:
                    return
            await message.edit(suppress=True)


@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None:
        await connect(after)
        return

    if after.channel is None:
        await disconnect(before)
        return

    if before.channel != after.channel:
        await move(before, after)


async def connect(after):
    if len(after.channel.members) == 1 and after.channel.category_id == category_id:
        for channel in category.voice_channels:
            if len(channel.members) == 0:
                return
        await category.voice_channels[0].clone(name=random.choice(prefix) + random.choice(suffix))


async def disconnect(before):
    if len([c for c in category.voice_channels if len(c.members) == 0]) == 1:
        return
    if len(category.voice_channels) > 1 and len(
            before.channel.members) == 0 and before.channel.category_id == category_id:
        await before.channel.delete()


async def move(before, after):
    await connect(after)
    await disconnect(before)


client.run(TOKEN)
