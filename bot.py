#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import random
import re

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

global category
random.seed()

secrets_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'secrets.json')
with open(secrets_file, 'r') as sec:
    TOKEN = json.load(sec)["TOKEN"]

vanity_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vanity_roles.json')

config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config_dev.json')
with open(config_file, 'r') as file:
    config = json.load(file)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


@slash.slash(name="gru", guild_ids=[config["server_id"]], description="Assign yourself vanity role.",
             options=[
                 create_option(
                     name="name",
                     description="This is the name of the role.",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="color",
                     description="This is the color of the role.",
                     option_type=3,
                     required=True
                 )
             ])
async def gru(ctx, name: str, color: str):
    if not re.match(r"^#[a-fA-F0-9]{6}$", color) or re.match(r"^[a-zß]", name):
        await ctx.send(
            content=f"**Invalid input:** '{name}, {color}'\n"
                    f"`name` is not allowed to start with a lowercase letter\n"
                    f"`color` needs to be a six digit hexadecimal number beginning with a '#'.")
        return

    with open(vanity_file, 'r') as fp:
        data = json.load(fp)

    guild = ctx.guild
    if str(ctx.author.id) in data:
        role_id = data[str(ctx.author.id)]
        role = guild.get_role(role_id)

        await role.edit(name=name, color=discord.Colour(int(color[1:], 16)), reason="Edited vanity role")
        await ctx.send(content=f"Edited role of {ctx.author.name} to {name}, {color}")
    else:
        new_role = await guild.create_role(name=name, colour=discord.Colour(int(color[1:], 16)),
                                           reason='Created vanity role')

        user = ctx.author
        await user.add_roles(new_role, reason='Added vanity role')

        data[str(ctx.author.id)] = new_role.id
        with open(vanity_file, 'w') as fp:
            json.dump(data, fp, sort_keys=True, indent=4)
        await ctx.send(content=f"Added role {name}, {color} to {ctx.author.name}")


@slash.slash(name="ungru", guild_ids=[config["server_id"]], description="Remove vanity role",
             options=[
                 create_option(
                     name="user",
                     description="This is the username (Admin only)",
                     option_type=6,
                     required=False
                 ),
                 create_option(
                     name="reason",
                     description="This is the reason (Admin only)",
                     option_type=3,
                     required=False
                 )
             ])
async def ungru(ctx, user=None, reason=None):
    if (user or reason) and not ctx.guild.get_role(config["admin_role_id"]) in ctx.author.roles:
        await ctx.send(content=f"Hallo {ctx.author.name}. Du Kek hast nicht die Rechte! <:honkler:721352866127675413>")
        return

    if not user and reason:
        await ctx.send(
            content=f"Hallo {ctx.author.name}. Du Kek hast den user vergessen! <:honkler:721352866127675413>")
        return

    if user:
        with open(vanity_file, 'r') as fp:
            data = json.load(fp)

        if str(user.id) not in data:
            await ctx.send(content=f"This user does not have a vanity role.")
            return

        roleid = data[str(user.id)]
        del data[str(user.id)]
        with open(vanity_file, 'w') as fp:
            json.dump(data, fp, sort_keys=True, indent=4)

        role = ctx.guild.get_role(roleid)
        await role.delete(reason=f"Removed by {ctx.author.name}. Reason: {reason}")
        await ctx.send(content=f"Removed {user}'s vanity role: {role}. Reason being: {reason}")
    else:
        with open(vanity_file, 'r') as fp:
            data = json.load(fp)

        if str(ctx.author.id) not in data:
            await ctx.send(content=f"You do not have a vanity role.")
            return

        roleid = data[str(ctx.author.id)]
        del data[str(ctx.author.id)]

        with open(vanity_file, 'w') as fp:
            json.dump(data, fp, sort_keys=True, indent=4)

        role = ctx.guild.get_role(roleid)
        await role.delete(reason=f"Removed by {ctx.author.name}.")
        await ctx.send(content=f"Successfully removed your vanity role: {role}")


@bot.event
async def on_ready():
    global category
    print(f'{bot.user} has connected to Discord!')
    guild = next(g for g in bot.guilds if g.id == config["server_id"])
    category = next(c for c in guild.categories if c.id == config["dynamic_category_id"])

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='over the inn'))


@bot.event
async def on_message(message):
    for channel in config["moderated_channels"]:
        if message.channel.id == channel:
            for link in config["whitelisted_previews"]:
                if link in message.content:
                    return
            await message.edit(suppress=True)


@bot.event
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
    if len(after.channel.members) == 1 and after.channel.category_id == config["dynamic_category_id"]:
        for channel in category.voice_channels:
            if len(channel.members) == 0:
                return
        await category.voice_channels[0].clone(
            name=random.choice(config["channel_name_prefix"]) + random.choice(config["channel_name_suffix"]))


async def disconnect(before):
    if len([c for c in category.voice_channels if len(c.members) == 0]) == 1:
        return
    if len(category.voice_channels) > 1 and len(
            before.channel.members) == 0 and before.channel.category_id == config["dynamic_category_id"]:
        await before.channel.delete()


async def move(before, after):
    await connect(after)
    await disconnect(before)


bot.run(TOKEN)
