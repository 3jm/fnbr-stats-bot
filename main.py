import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ButtonStyle, Webhook
from nextcord.abc import GuildChannel
from nextcord.ui import Button, View
import requests
import json
import os
import time
import datetime
import asyncio
import aiohttp
import colorama
import random
from datetime import datetime, timedelta
from aiohttp import request
from aiohttp import ClientSession
from colorama import Fore, Back, Style
from captcha.image import ImageCaptcha
colorama.init()

token = ""
api_key = ""
intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)
bot.remove_command('help')
testing_guild_id = 0

@bot.event
async def on_ready():
    print("ready")


list_of_platforms = [
    "epic",
    "psn",
    "xbl"
]


@bot.slash_command(guild_ids=[testing_guild_id])
async def fnbr(interaction: Interaction, *, username, platform: str = SlashOption(name="platform", choices=list_of_platforms)):
    headers = {
        "Authorization": api_key
    }
    r = requests.get(f'https://fortnite-api.com/v2/stats/br/v2?name={username}&accountType={platform}', headers=headers)
    data = r.json()
    if data["status"] == 200:
        tot_mins = data["data"]["stats"]["all"]["overall"]["minutesPlayed"]
        hours = tot_mins // 60
        time_string = "{}".format(hours, tot_mins)
        embed = nextcord.Embed(
            title = f'{data["data"]["account"]["name"]}\'s Fortnite Stats'
        )
        embed.add_field(name=f'Solo Win\'s', value=f'**{data["data"]["stats"]["all"]["solo"]["wins"]}**', inline=True)
        embed.add_field(name=f'Duo Win\'s', value=f'**{data["data"]["stats"]["all"]["duo"]["wins"]}**', inline=True)
        embed.add_field(name=f'Trio Win\'s', value=f'**null**', inline=True)
        embed.add_field(name=f'Squad Win\'s', value=f'**{data["data"]["stats"]["all"]["squad"]["wins"]}**', inline=True)
        embed.add_field(name=f'LTM Win\'s', value=f'**{data["data"]["stats"]["all"]["ltm"]["wins"]}**', inline=True)
        embed.add_field(name=f'K/D Ratio', value=f'**{data["data"]["stats"]["all"]["overall"]["kd"]}**', inline=True)
        embed.add_field(name=f'Total Win\'s', value=f'**{data["data"]["stats"]["all"]["overall"]["wins"]}**')
        embed.add_field(name=f'Total Kill\'s', value=f'**{data["data"]["stats"]["all"]["overall"]["kills"]}**')
        embed.add_field(name=f'Win Percentage', value=f'**{data["data"]["stats"]["all"]["overall"]["winRate"]}**')
        embed.add_field(name=f'Hours Played', value=f'**{data["data"]["account"]["name"]}** has **{time_string}** hours on record.')
        embed.set_footer(text=f'Ark • 2021 | Trio\'s stats will ALWAYS be NULL', icon_url='https://cdn.discordapp.com/avatars/922333929367810118/60bb9cc3d1b516d94a95cdf9bcd68f49.png?size=256')
        await interaction.response.send_message(embed = embed)

    elif data["status"] == 400:
        er = nextcord.Embed(
            title = f'Error {data["status"]}',
            description = f"{data['error']}\n\nSupported Platforms: `epic`,`psn`,`xbl` are letter sensitive."
        )
        er.set_thumbnail(url='https://pbs.twimg.com/media/FJ4nMuGVUAIoYk7?format=jpg&name=small')
        er.set_footer(text=f'Ark • 2021', icon_url='https://cdn.discordapp.com/avatars/922333929367810118/60bb9cc3d1b516d94a95cdf9bcd68f49.png?size=256')
        await interaction.response.send_message(embed = er, ephemeral = True)

    elif data["status"] == 403:
        eer = nextcord.Embed(
            title = f'Error {data["status"]}',
            description = f"{data['error']}"
        )
        eer.set_thumbnail(url='https://pbs.twimg.com/media/FKUN1o5XIAI0zsR?format=jpg&name=large')
        eer.set_footer(text=f'Ark • 2021', icon_url='https://cdn.discordapp.com/avatars/922333929367810118/60bb9cc3d1b516d94a95cdf9bcd68f49.png?size=256')
        await interaction.response.send_message(embed = eer, ephemeral = True)
        
    elif data["status"] == 404:
        eerr = nextcord.Embed(
            title = f'Error {data["status"]}',
            description = f"{data['error']}"
        )
        eerr.set_thumbnail(url='https://cdn.discordapp.com/attachments/916471148026425397/939638532480311347/imgonline-com-ua-ReplaceColor-mwBVeCifK3P0HF.jpg')
        eerr.set_footer(text=f'Ark • 2021', icon_url='https://cdn.discordapp.com/avatars/922333929367810118/60bb9cc3d1b516d94a95cdf9bcd68f49.png?size=256')
        await interaction.response.send_message(embed = eerr, ephemeral = True)

bot.run(token)
